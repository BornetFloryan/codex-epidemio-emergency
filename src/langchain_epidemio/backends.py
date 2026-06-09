"""Centralized selection of the LLM and embeddings backends."""

from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv


def _backend() -> str:
    load_dotenv()
    backend = os.getenv("LLM_BACKEND", "mistral").strip().lower()
    if backend not in {"mistral", "ollama"}:
        raise ValueError("LLM_BACKEND doit valoir 'mistral' ou 'ollama'.")
    return backend


def get_llm(temperature: float = 0) -> Any:
    """Return the configured LangChain chat model."""
    backend = _backend()

    if backend == "mistral":
        from langchain_mistralai import ChatMistralAI

        if not os.getenv("MISTRAL_API_KEY"):
            raise RuntimeError("MISTRAL_API_KEY est absente. La definir dans le fichier .env.")
        return ChatMistralAI(
            model=os.getenv("MISTRAL_MODEL", "mistral-small-latest"),
            temperature=temperature,
        )

    from langchain_ollama import ChatOllama

    return ChatOllama(
        model=os.getenv("OLLAMA_MODEL", "qwen3:4b"),
        temperature=temperature,
    )


def get_embeddings() -> Any:
    """Return embeddings matching the configured LLM backend."""
    backend = _backend()

    if backend == "mistral":
        from langchain_mistralai import MistralAIEmbeddings

        if not os.getenv("MISTRAL_API_KEY"):
            raise RuntimeError("MISTRAL_API_KEY est absente. La definir dans le fichier .env.")
        return MistralAIEmbeddings(model=os.getenv("MISTRAL_EMBED_MODEL", "mistral-embed"))

    from langchain_ollama import OllamaEmbeddings

    return OllamaEmbeddings(model=os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text"))
