from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("langchain")

from langchain_core.embeddings import FakeEmbeddings

from src.langchain_epidemio.agent import build_agent
from src.langchain_epidemio.models import SituationAssessment
from src.langchain_epidemio.rag import load_documents, split_documents
from src.langchain_epidemio.tools import analyser_tendance, produire_note_de_crise
from src.langchain_epidemio.workflow import build_workflow, plan_workflow


def test_existing_skills_are_callable_as_langchain_tools():
    trend = analyser_tendance.invoke({"values": [10, 12, 15]})
    report = produire_note_de_crise.invoke({"information": "Hausse des syndromes grippaux."})

    assert trend["status"] == "ok"
    assert trend["trend"] == "increasing"
    assert report["status"] == "ok"
    assert report["limits"]


def test_structured_assessment_rejects_unknown_attention_level():
    with pytest.raises(ValueError):
        SituationAssessment(
            summary="Signal a verifier",
            attention_level="urgent",
        )


def test_rag_documents_keep_source_metadata(tmp_path: Path):
    source = tmp_path / "source.md"
    source.write_text("# Surveillance\nLa tendance est en hausse.", encoding="utf-8")

    documents = load_documents([source])
    chunks = split_documents(documents, chunk_size=30, chunk_overlap=5)

    assert chunks
    assert all(chunk.metadata["source"] == str(source) for chunk in chunks)


def test_fake_embeddings_are_available_for_offline_rag_tests():
    embeddings = FakeEmbeddings(size=8)
    assert len(embeddings.embed_query("veille epidemiologique")) == 8


def test_pdf_loader_reads_course_pdf():
    documents = load_documents([Path("AgentsLangchain.pdf").resolve()])

    assert documents
    assert "Agents IA" in documents[0].page_content
    assert documents[0].metadata["source"].endswith("AgentsLangchain.pdf")


def test_agent_graph_builds_without_network(monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "ollama")

    graph = build_agent().get_graph()

    assert "model" in graph.nodes
    assert "tools" in graph.nodes


def test_workflow_planning_is_deterministic():
    question = "Analyse la hausse 12, 15, 18 de la grippe avec la meteo de Besancon"
    plans = [plan_workflow(question) for _ in range(5)]

    assert plans == [["surveillance", "tendance", "territoire", "synthese"]] * 5


def test_workflow_plans_always_end_with_synthesis():
    questions = [
        "Analyse la tendance 12, 15, 18",
        "Trouve des sources sur la grippe",
        "Donne la meteo de Besancon",
        "Question generale sans mot-cle",
    ]

    assert all(plan_workflow(question)[-1] == "synthese" for question in questions)


def test_documentation_agent_is_only_selected_when_rag_is_enabled():
    question = "Recherche les consignes dans la documentation du projet"

    assert "documentation" not in plan_workflow(question, include_rag=False)
    assert "documentation" in plan_workflow(question, include_rag=True)


def test_multi_agent_workflow_graph_builds_without_network(monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "ollama")

    graph = build_workflow().get_graph()

    assert {"planification", "surveillance", "tendance", "territoire", "synthese", "avancer"} <= set(
        graph.nodes
    )
