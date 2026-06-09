"""LangChain tools wrapping the existing Codex skill scripts."""

from __future__ import annotations

import importlib.util
from functools import lru_cache
from pathlib import Path
from types import ModuleType

from langchain_core.tools import BaseTool, tool

ROOT_DIR = Path(__file__).resolve().parents[2]
SKILLS_DIR = ROOT_DIR / ".codex" / "skills"


@lru_cache(maxsize=None)
def _load_skill(skill_name: str) -> ModuleType:
    path = SKILLS_DIR / skill_name / "main.py"
    spec = importlib.util.spec_from_file_location(f"epidemio_skill_{skill_name.replace('-', '_')}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Impossible de charger le skill {skill_name}.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@tool
def rechercher_donnees_sanitaires(query: str) -> dict:
    """Recherche des jeux de donnees sanitaires publics pertinents sur data.gouv.fr."""
    return _load_skill("health-dataset-search").build_response(query)


@tool
def consulter_indicateur_ias(indicator: str) -> dict:
    """Consulte un indicateur avance sanitaire. indicator doit valoir grippe ou gastro."""
    normalized = indicator.strip().lower()
    if normalized not in {"grippe", "gastro"}:
        return {
            "status": "error",
            "message": "L'indicateur doit valoir 'grippe' ou 'gastro'.",
            "limits": ["Aucun diagnostic medical individuel ne peut etre produit."],
        }
    return _load_skill("ias-indicators").build_response(normalized)


@tool
def analyser_tendance(values: list[float]) -> dict:
    """Analyse une serie numerique et qualifie sa tendance epidemiologique recente."""
    return _load_skill("trend-analysis").analyze(values)


@tool
def contexte_geographique(place: str) -> dict:
    """Retourne le contexte geographique d'une commune francaise ou d'un code postal."""
    return _load_skill("geo-zone-context").build_response(place)


@tool
def contexte_meteorologique(place: str) -> dict:
    """Retourne le contexte meteorologique actuel d'une commune francaise."""
    return _load_skill("weather-alert-context").build_response(place)


@tool
def produire_note_de_crise(information: str) -> dict:
    """Produit une courte note de situation a partir d'informations epidemiologiques."""
    return _load_skill("crisis-report").build_report(information)


def get_tools(extra_tools: list[BaseTool] | None = None) -> list[BaseTool]:
    """Return the focused set of tools available to the agent."""
    tools: list[BaseTool] = [
        rechercher_donnees_sanitaires,
        consulter_indicateur_ias,
        analyser_tendance,
        contexte_geographique,
        contexte_meteorologique,
        produire_note_de_crise,
    ]
    if extra_tools:
        tools.extend(extra_tools)
    return tools
