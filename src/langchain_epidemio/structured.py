"""Structured-output chain for a validated situation assessment."""

from __future__ import annotations

from typing import Any

from langchain_core.prompts import ChatPromptTemplate

from .backends import get_llm
from .models import SituationAssessment

SYSTEM_PROMPT = """
Tu es un assistant de veille epidemiologique en situation d'urgence.
Tu aides a qualifier les informations, mais tu ne fournis jamais de diagnostic medical individuel.
Mentionne les sources officielles a verifier et les limites des donnees.
Si les informations sont insuffisantes, choisis le niveau d'attention indetermine.
""".strip()


def build_structured_chain(llm: Any | None = None) -> Any:
    """Build a prompt -> model -> validated Pydantic output chain."""
    model = (llm or get_llm(temperature=0)).with_structured_output(SituationAssessment)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", "Evalue la situation suivante :\n\n{situation}"),
        ]
    )
    return prompt | model


def assess_situation(situation: str, llm: Any | None = None) -> SituationAssessment:
    """Return a validated assessment for the provided situation."""
    return build_structured_chain(llm).invoke({"situation": situation})
