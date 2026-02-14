"""
LIA V3 — Intake Agent (CORE).
Reemplaza Extractor + Router + Architect de V2.

Recibe el PDF nativo (visión de Gemini) y produce:
- Clasificación del dominio
- Extracción de estructura completa (partes, fechas, valores)
NOTA: NO extrae el texto completo — el Auditor lee el PDF directamente.
"""
import logging

from google.adk.agents import LlmAgent

from schemas import IntakeOutput
from prompt_builder import create_instruction_provider
import config

logger = logging.getLogger(__name__)

# =============================================================================
# INSTRUCCIÓN BASE
# =============================================================================

INTAKE_INSTRUCTION = """
Eres el AGENTE DE INTAKE de LIA (Legal Intelligence Agent).
Recibes el PDF del contrato y produces una clasificación + extracción estructural.

## TAREA 1: CLASIFICACIÓN
Clasifica el contrato usando las SEÑALES DE CLASIFICACIÓN del documento
"Tipos de Contratos Soportados" inyectado en tu knowledge.

- Usa las señales textuales para determinar el tipo de contrato
- Si confidence_score < 0.8, clasifica como 'contrato_general'
- Cita texto del contrato en detected_signals como evidencia

## TAREA 2: EXTRACCIÓN ESTRUCTURAL
Extrae los datos estructurales según el CHECKLIST DE EXTRACCIÓN
del dominio inyectado en tu knowledge. El checklist define qué
elementos son esenciales vs importantes y cómo evaluar completitud.

## PERSPECTIVA DEL USUARIO
Configuración de sesión: {session_config}
Esto NO afecta la clasificación pero SÍ el enfoque de la extracción.

## FORMATO
Responde EXCLUSIVAMENTE con el JSON que cumple el schema IntakeOutput.
"""

# =============================================================================
# AGENTE
# =============================================================================

intake_agent = LlmAgent(
    name="lia_intake",
    model=config.MODELS["intake"],
    description="Clasifica el contrato y extrae estructura completa. NO extrae texto — Auditor lee PDF directo.",
    instruction=create_instruction_provider("intake", INTAKE_INSTRUCTION),
    output_schema=IntakeOutput,
    output_key="intake_output",
    include_contents="default",  # Necesita ver el PDF del usuario
)
