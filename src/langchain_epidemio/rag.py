"""Minimal RAG over the project's local Markdown documentation."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_core.tools import BaseTool, tool
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .backends import get_embeddings

ROOT_DIR = Path(__file__).resolve().parents[2]


def documentation_paths(root: Path = ROOT_DIR) -> list[Path]:
    """Return the local project documentation used by the RAG."""
    paths = [root / "README.md", root / "AGENTS.md"]
    paths.extend(sorted((root / ".codex" / "skills").glob("*/SKILL.md")))
    paths.extend(sorted((root / ".codex" / "skills").glob("*/references/*.md")))
    return [path for path in paths if path.is_file()]


def load_documents(paths: Iterable[Path] | None = None) -> list[Document]:
    """Load Markdown or PDF files as LangChain documents with source metadata."""
    selected_paths = list(paths) if paths is not None else documentation_paths()
    documents = []

    for path in selected_paths:
        if path.suffix.lower() == ".pdf":
            documents.extend(PyPDFLoader(str(path)).load())
            continue
        documents.append(
            Document(
                page_content=path.read_text(encoding="utf-8"),
                metadata={
                    "source": str(path.relative_to(ROOT_DIR)) if path.is_relative_to(ROOT_DIR) else str(path)
                },
            )
        )

    return documents


def split_documents(
    documents: list[Document],
    chunk_size: int = 800,
    chunk_overlap: int = 120,
) -> list[Document]:
    """Split documents into overlapping chunks suitable for retrieval."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(documents)


def build_vectorstore(
    embeddings: Any | None = None,
    paths: Iterable[Path] | None = None,
) -> InMemoryVectorStore:
    """Build an in-memory vector store from Markdown or PDF documentation."""
    chunks = split_documents(load_documents(paths))
    return InMemoryVectorStore.from_documents(chunks, embeddings or get_embeddings())


def build_documentation_tool(
    vectorstore: InMemoryVectorStore | None = None,
    k: int = 4,
) -> BaseTool:
    """Build the agentic RAG search tool."""
    store = vectorstore or build_vectorstore()

    @tool
    def rechercher_documentation_epidemio(question: str) -> str:
        """Recherche dans la documentation locale du projet de veille epidemiologique."""
        documents = store.similarity_search(question, k=k)
        return "\n\n---\n\n".join(
            f"Source: {doc.metadata.get('source', 'inconnue')}\n{doc.page_content}" for doc in documents
        )

    return rechercher_documentation_epidemio
