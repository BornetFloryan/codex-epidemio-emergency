"""Command-line interface for the epidemiological LangChain agent."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .structured import assess_situation
from .workflow import build_workflow, invoke_workflow, stream_workflow


def _print_json(value: Any) -> None:
    if hasattr(value, "model_dump"):
        value = value.model_dump()
    print(json.dumps(value, ensure_ascii=False, indent=2))


def _interactive(workflow: Any, thread_id: str) -> None:
    print("Workflow epidemiologique pret. Entrez 'quit' pour terminer.")
    while True:
        question = input("\n> ").strip()
        if question.lower() in {"quit", "exit"}:
            return
        if question:
            _print_json(invoke_workflow(workflow, question, thread_id))


def _main() -> None:
    parser = argparse.ArgumentParser(description="Workflow LangGraph multi-agents de veille epidemiologique.")
    parser.add_argument("question", nargs="*", help="Question a transmettre au workflow")
    parser.add_argument("--thread-id", default="default", help="Identifiant de conversation")
    parser.add_argument("--rag", action="store_true", help="Activer le RAG sur la documentation locale")
    parser.add_argument(
        "--rag-pdf",
        action="append",
        type=Path,
        default=[],
        help="Indexer un PDF dans le RAG ; option repetable",
    )
    parser.add_argument("--stream", action="store_true", help="Afficher les etapes du graphe")
    parser.add_argument("--interactive", action="store_true", help="Demarrer une conversation multi-tour")
    parser.add_argument(
        "--structured",
        action="store_true",
        help="Produire une evaluation validee par un schema Pydantic",
    )
    args = parser.parse_args()

    question = " ".join(args.question).strip()
    if args.structured:
        if not question:
            parser.error("--structured necessite une description de situation.")
        _print_json(assess_situation(question))
        return

    workflow = build_workflow(
        include_rag=args.rag or bool(args.rag_pdf),
        rag_paths=args.rag_pdf or None,
    )
    if args.interactive:
        _interactive(workflow, args.thread_id)
        return
    if not question:
        parser.error("Une question est necessaire hors mode --interactive.")

    if args.stream:
        for update in stream_workflow(workflow, question, args.thread_id):
            _print_json(update)
        return

    _print_json(invoke_workflow(workflow, question, args.thread_id))


def main() -> None:
    try:
        _main()
    except Exception as exc:
        _print_json(
            {
                "status": "error",
                "message": str(exc),
                "limits": [
                    "Verifier la configuration du backend et sa disponibilite.",
                    "Aucun diagnostic medical individuel ne peut etre produit.",
                ],
            }
        )


if __name__ == "__main__":
    main()
