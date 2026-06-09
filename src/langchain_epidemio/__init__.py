"""LangChain agent for epidemiological emergency monitoring."""

from .agent import build_agent
from .models import SituationAssessment

__all__ = ["SituationAssessment", "build_agent"]
