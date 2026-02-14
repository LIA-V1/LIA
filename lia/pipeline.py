"""
LIA V3 — Pipeline SequentialAgent.
Orquesta la ejecución secuencial de todos los agentes de análisis.

Pipeline: Intake → Auditor → Financial → Drafter → CEO → Reporter

Incluye callbacks a nivel pipeline para:
- Validación de state antes de cada agente
- Logging de ejecución después de cada sub-agente
"""
import logging

from google.adk.agents import SequentialAgent

from .agents import (
    intake_agent,
    auditor_agent,
    financial_agent,
    drafter_agent,
    ceo_agent,
    reporter_agent,
)
from .callbacks import validate_pipeline_state, log_agent_execution

logger = logging.getLogger(__name__)

# =============================================================================
# PIPELINE
# =============================================================================

pipeline = SequentialAgent(
    name="lia_pipeline",
    description=(
        "Pipeline secuencial de análisis contractual. "
        "Ejecuta: Intake → Auditor → Financial → Drafter → CEO → Reporter."
    ),
    sub_agents=[
        intake_agent,
        auditor_agent,
        financial_agent,
        drafter_agent,
        ceo_agent,
        reporter_agent,
    ],
    before_agent_callback=validate_pipeline_state,
    after_agent_callback=log_agent_execution,
)
