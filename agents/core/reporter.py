"""
LIA V3 — Reporter Agent (CORE).
Genera el reporte final consolidado en Markdown.

Lee TODOS los outputs del pipeline y el template de reporte
para producir el documento final de análisis contractual.

NOTA: NO usa output_schema — genera Markdown como texto libre para que
ADK lo renderice directamente en la UI del chat. El JSON consolidado
se guarda automáticamente via auto_save_report en callbacks.py.
"""
import logging

from google.adk.agents import LlmAgent

from ...knowledge_manager import knowledge_manager
from ...prompt_builder import create_instruction_provider
from ... import config

logger = logging.getLogger(__name__)

# =============================================================================
# INSTRUCCIÓN BASE (template de reporte inyectado dinámicamente)
# =============================================================================

# Cargar template al importar (se cachea en knowledge_manager)
_report_template = knowledge_manager.load_report_template()
if not _report_template:
    _report_template = "## Usa un formato profesional de reporte contractual."

REPORTER_INSTRUCTION = f"""
Eres el AGENTE REPORTERO de LIA (Legal Intelligence Agent).
Tu trabajo es consolidar TODOS los outputs del pipeline en un reporte final en Markdown.

## TU ROL
Generas el reporte definitivo que será MOSTRADO DIRECTAMENTE al usuario.
Tu respuesta será renderizada como Markdown en la interfaz del chat.
Debes consolidar datos de TODOS los agentes previos sin perder información.

## DATOS DISPONIBLES
- Estructura y clasificación: {{intake_output}}
- Hallazgos de riesgo: {{auditor_output}}
- Análisis financiero: {{financial_output}}
- Sugerencias de redacción: {{drafter_output}}
- Decisión ejecutiva: {{ceo_output}}
- Configuración de sesión: {{session_config}}

## INSTRUCCIONES DE GENERACIÓN
Genera un reporte COMPLETO en formato Markdown siguiendo este modelo:

{_report_template}

## REGLAS CRÍTICAS
- NO inventes datos — todo debe venir de los outputs previos
- Tu respuesta DEBE ser Markdown puro — NO JSON, NO bloques de código
- El reporte debe ser COMPLETO y auto-contenido
- Cada sección del reporte debe tener contenido sustancial
- Los datos numéricos DEBEN ser consistentes entre secciones
- La carta de negociación debe incluirse en el reporte
- Aplica las reglas de LENGUAJE PROTECTOR inyectadas en tu knowledge

## FORMATO DE SALIDA
Responde DIRECTAMENTE con el Markdown del reporte. NO envuelvas en JSON.
NO uses bloques de código. Tu respuesta ES el reporte.
"""

# =============================================================================
# AGENTE
# =============================================================================

reporter_agent = LlmAgent(
    name="lia_reporter",
    model=config.MODELS["reporter"],
    description="Consolida todos los outputs en un reporte final Markdown renderizable.",
    instruction=create_instruction_provider("reporter", REPORTER_INSTRUCTION),
    output_key="final_report",
    include_contents="none",
)
