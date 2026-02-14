"""
LIA V3 — Agents Package.
Organización:
- core/: Agentes fundamentales del pipeline (Intake, Reporter)
- team/: Agentes analíticos especializados (Auditor, Financial, Drafter, CEO)
"""
from .core.intake import intake_agent
from .core.reporter import reporter_agent
from .team.auditor import auditor_agent
from .team.financial import financial_agent
from .team.drafter import drafter_agent
from .team.ceo import ceo_agent

__all__ = [
    "intake_agent",
    "reporter_agent",
    "auditor_agent",
    "financial_agent",
    "drafter_agent",
    "ceo_agent",
]
