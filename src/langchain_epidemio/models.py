"""Pydantic schemas used for validated LLM outputs."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class SituationAssessment(BaseModel):
    """Validated operational assessment generated from a situation description."""

    summary: str = Field(description="Resume factuel et concis de la situation")
    attention_level: Literal["faible", "modere", "eleve", "critique", "indetermine"] = Field(
        description="Niveau d'attention, sans constituer un diagnostic medical"
    )
    signals_to_monitor: list[str] = Field(
        default_factory=list,
        description="Signaux epidemiologiques, geographiques ou meteo a surveiller",
    )
    recommended_actions: list[str] = Field(
        default_factory=list,
        description="Actions prudentes de verification ou de suivi",
    )
    sources_to_verify: list[str] = Field(
        default_factory=list,
        description="Sources officielles a consulter",
    )
    limits: list[str] = Field(
        default_factory=list,
        description="Limites des donnees et de l'analyse",
    )
