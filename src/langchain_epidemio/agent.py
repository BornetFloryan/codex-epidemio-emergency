"""Creation and execution helpers for the epidemiological LangChain agent."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Iterator

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from .backends import get_llm
from .rag import build_documentation_tool, build_vectorstore
from .tools import get_tools

SYSTEM_PROMPT = """
Tu es un agent de veille epidemiologique pour l'aide a la decision en situation d'urgence.

Regles obligatoires :
- utilise les outils lorsque la demande necessite des donnees, une tendance ou un contexte local ;
- distingue les faits observes, les interpretations et les inconnues ;
- mentionne toujours les sources utilisees et les limites des donnees ;
- ne fournis jamais de diagnostic medical individuel ;
- privilegie une reponse courte, factuelle et operationnelle ;
- en cas d'incertitude, indique clairement ce qui doit etre verifie.
""".strip()


def build_agent(
    model: Any | None = None,
    include_rag: bool = False,
    checkpointer: Any | None = None,
    rag_paths: Iterable[Path] | None = None,
) -> Any:
    """Build the tool-calling agent with optional local documentation RAG."""
    extra_tools = []
    if include_rag:
        vectorstore = build_vectorstore(paths=rag_paths)
        extra_tools.append(build_documentation_tool(vectorstore))
    return create_agent(
        model=model or get_llm(temperature=0),
        tools=get_tools(extra_tools),
        system_prompt=SYSTEM_PROMPT,
        checkpointer=checkpointer or InMemorySaver(),
    )


def invoke_agent(agent: Any, question: str, thread_id: str = "default") -> dict:
    """Invoke the agent while preserving memory for a conversation thread."""
    return agent.invoke(
        {"messages": [{"role": "user", "content": question}]},
        config={
            "configurable": {"thread_id": thread_id},
            "recursion_limit": 12,
        },
    )


def stream_agent(agent: Any, question: str, thread_id: str = "default") -> Iterator[Any]:
    """Stream complete graph states to expose the agent trajectory."""
    yield from agent.stream(
        {"messages": [{"role": "user", "content": question}]},
        config={
            "configurable": {"thread_id": thread_id},
            "recursion_limit": 12,
        },
        stream_mode="values",
    )


def final_content(result: dict) -> str:
    """Extract the final text content from an agent result."""
    messages = result.get("messages") or []
    return str(messages[-1].content) if messages else ""
