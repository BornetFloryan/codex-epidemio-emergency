"""Deterministic multi-agent workflow for epidemiological monitoring."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterable, Literal, TypedDict

from langchain.agents import create_agent
from langchain_core.messages import ToolMessage
from langchain_core.tools import BaseTool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from .backends import get_llm
from .rag import build_documentation_tool, build_vectorstore
from .tools import (
    analyser_tendance,
    consulter_indicateur_ias,
    contexte_geographique,
    contexte_meteorologique,
    produire_note_de_crise,
    rechercher_donnees_sanitaires,
)

AgentName = Literal["surveillance", "tendance", "territoire", "documentation", "synthese"]

AGENT_ORDER: tuple[AgentName, ...] = (
    "surveillance",
    "tendance",
    "territoire",
    "documentation",
    "synthese",
)

COMMON_RULES = """
Regles obligatoires :
- utilise les outils disponibles pour etablir les faits ;
- distingue les faits, les interpretations et les inconnues ;
- cite les sources et les limites retournees par les outils ;
- ne fournis jamais de diagnostic medical individuel ;
- reste court, factuel et operationnel.
""".strip()

AGENT_CONFIG: dict[AgentName, tuple[str, list[BaseTool]]] = {
    "surveillance": (
        "Tu es l'agent de surveillance sanitaire. Recherche les sources publiques et les indicateurs IAS utiles.",
        [rechercher_donnees_sanitaires, consulter_indicateur_ias],
    ),
    "tendance": (
        "Tu es l'agent d'analyse de tendance. Extrais les valeurs de la demande et qualifie leur evolution.",
        [analyser_tendance],
    ),
    "territoire": (
        "Tu es l'agent de contexte territorial. Etablis le contexte geographique et meteorologique utile.",
        [contexte_geographique, contexte_meteorologique],
    ),
    "documentation": (
        "Tu es l'agent documentaire. Recherche uniquement dans la documentation locale indexee.",
        [],
    ),
    "synthese": (
        "Tu es l'agent de synthese de crise. Produis la note finale a partir des constats transmis.",
        [produire_note_de_crise],
    ),
}


class WorkflowState(TypedDict, total=False):
    """Shared state passed through the deterministic graph."""

    question: str
    plan: list[AgentName]
    cursor: int
    findings: list[dict[str, Any]]
    trace: list[str]
    final_answer: str


def plan_workflow(question: str, include_rag: bool = False) -> list[AgentName]:
    """Select specialist agents with explicit deterministic rules."""
    normalized = question.lower()
    selected: set[AgentName] = set()

    if re.search(r"\d+(?:[.,]\d+)?(?:\s*[,;]\s*|\s+)\d+", normalized) or any(
        word in normalized
        for word in ("tendance", "evolution", "évolution", "hausse", "baisse", "stable", "incidence")
    ):
        selected.add("tendance")

    if any(
        word in normalized
        for word in (
            "grippe",
            "grippal",
            "gastro",
            "epidem",
            "épidém",
            "sanitaire",
            "indicateur",
            "donnee",
            "donnée",
            "source",
        )
    ):
        selected.add("surveillance")

    if any(
        word in normalized
        for word in (
            "meteo",
            "météo",
            "temperature",
            "température",
            "pluie",
            "vent",
            "commune",
            "departement",
            "département",
            "region",
            "région",
            "zone",
            "ville",
        )
    ):
        selected.add("territoire")

    if include_rag and any(
        word in normalized
        for word in ("documentation", "document", "pdf", "cours", "skill", "consigne", "projet")
    ):
        selected.add("documentation")

    if not selected:
        selected.add("surveillance")

    selected.add("synthese")
    return [agent for agent in AGENT_ORDER if agent in selected]


def _final_content(result: dict[str, Any]) -> str:
    messages = result.get("messages") or []
    return str(messages[-1].content) if messages else ""


def _tool_outputs(result: dict[str, Any]) -> list[Any]:
    outputs: list[Any] = []
    for message in result.get("messages") or []:
        if not isinstance(message, ToolMessage):
            continue
        content = message.content
        if isinstance(content, str):
            try:
                content = json.loads(content)
            except json.JSONDecodeError:
                pass
        outputs.append(content)
    return outputs


def _context_for_agent(state: WorkflowState) -> str:
    findings = state.get("findings") or []
    if not findings:
        return state["question"]
    return (
        f"Demande initiale : {state['question']}\n\n"
        "Constats des agents precedents :\n"
        f"{json.dumps(findings, ensure_ascii=False, default=str)}"
    )


def _build_specialist_agents(
    model: Any,
    include_rag: bool,
    rag_paths: Iterable[Path] | None,
) -> dict[AgentName, Any]:
    configs = dict(AGENT_CONFIG)
    if include_rag:
        documentation_tool = build_documentation_tool(build_vectorstore(paths=rag_paths))
        prompt, _ = configs["documentation"]
        configs["documentation"] = (prompt, [documentation_tool])

    agents: dict[AgentName, Any] = {}
    for name, (prompt, tools) in configs.items():
        if name == "documentation" and not tools:
            continue
        agents[name] = create_agent(
            model=model,
            tools=tools,
            system_prompt=f"{prompt}\n\n{COMMON_RULES}",
            name=f"agent_{name}",
        )
    return agents


def build_workflow(
    model: Any | None = None,
    include_rag: bool = False,
    checkpointer: Any | None = None,
    rag_paths: Iterable[Path] | None = None,
) -> Any:
    """Build the outer deterministic graph and its five specialist agents."""
    specialists = _build_specialist_agents(
        model=model or get_llm(temperature=0),
        include_rag=include_rag,
        rag_paths=rag_paths,
    )

    def planner(state: WorkflowState) -> dict[str, Any]:
        plan = plan_workflow(state["question"], include_rag=include_rag)
        return {"plan": plan, "cursor": 0, "findings": [], "trace": ["planification"]}

    def run_specialist(name: AgentName):
        def node(state: WorkflowState) -> dict[str, Any]:
            result = specialists[name].invoke(
                {"messages": [{"role": "user", "content": _context_for_agent(state)}]}
            )
            finding = {
                "agent": name,
                "answer": _final_content(result),
                "tool_outputs": _tool_outputs(result),
            }
            update: dict[str, Any] = {
                "findings": [*(state.get("findings") or []), finding],
                "trace": [*(state.get("trace") or []), name],
            }
            if name == "synthese":
                update["final_answer"] = finding["answer"]
            return update

        return node

    def advance(state: WorkflowState) -> dict[str, int]:
        return {"cursor": state.get("cursor", 0) + 1}

    def next_agent(state: WorkflowState) -> AgentName | Literal["end"]:
        cursor = state.get("cursor", 0)
        plan = state.get("plan") or []
        return plan[cursor] if cursor < len(plan) else "end"

    graph = StateGraph(WorkflowState)
    graph.add_node("planification", planner)
    for name in AGENT_ORDER:
        if name in specialists:
            graph.add_node(name, run_specialist(name))
    graph.add_node("avancer", advance)

    graph.add_edge(START, "planification")
    graph.add_conditional_edges(
        "planification",
        next_agent,
        {name: name for name in specialists} | {"end": END},
    )
    for name in specialists:
        graph.add_edge(name, "avancer")
    graph.add_conditional_edges(
        "avancer",
        next_agent,
        {name: name for name in specialists} | {"end": END},
    )
    return graph.compile(checkpointer=checkpointer or InMemorySaver())


def invoke_workflow(workflow: Any, question: str, thread_id: str = "default") -> dict[str, Any]:
    """Run the deterministic workflow while preserving state for the thread."""
    return workflow.invoke(
        {"question": question},
        config={"configurable": {"thread_id": thread_id}, "recursion_limit": 20},
    )


def stream_workflow(workflow: Any, question: str, thread_id: str = "default") -> Any:
    """Stream graph updates so the deterministic route is visible."""
    yield from workflow.stream(
        {"question": question},
        config={"configurable": {"thread_id": thread_id}, "recursion_limit": 20},
        stream_mode="updates",
    )
