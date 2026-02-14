"""
LIA V3 — Root Agent (Entry Point ADK).
Punto de entrada principal para 'adk web' y 'adk run'.

El root agent:
1. Recibe la perspectiva del usuario y el PDF del contrato
2. Llama set_session_config para guardar la perspectiva en state
3. Transfiere al pipeline secuencial para el análisis completo
"""
import logging

from google.adk.agents import LlmAgent

from pipeline import pipeline
from callbacks import auto_save_report
from knowledge_manager import knowledge_manager
from tools import set_session_config
import config

logger = logging.getLogger(__name__)

# =============================================================================
# ROOT AGENT INSTRUCTION
# =============================================================================

ROOT_INSTRUCTION = """
Eres LIA (Legal Intelligence Agent) V3, un sistema experto de análisis contractual.
Tu trabajo es recibir un contrato PDF y la perspectiva del usuario, y luego
iniciar el pipeline de análisis completo.

## FLUJO DE INTERACCIÓN

1. Si el usuario NO ha proporcionado perspectiva o PDF, PREGUNTA brevemente:
   - ¿Eres el contratante (comprador) o el contratista (vendedor/proveedor)?
   - El PDF del contrato

2. Una vez que tengas PERSPECTIVA + PDF, haz exactamente esto en orden:
   a. Llama la tool `set_session_config` con:
      - perspective: "contratante" o "contratista" según lo indicó el usuario dando una pequeña explicación breve de que es cada uno y como se podria identificarlo en el contrato
      - additional_context: cualquier contexto extra que haya dado (o "" si no dio)
   b. Luego transfiere el control a `lia_pipeline` para iniciar el análisis

## REGLAS
- Sé conciso y profesional
- NO analices el contrato tú mismo — eso lo hace el pipeline
- Solo necesitas la PERSPECTIVA y el PDF para iniciar
- Si el usuario proporciona todo de entrada, llama set_session_config y transfiere inmediatamente
- SIEMPRE llama set_session_config ANTES de transferir al pipeline
"""

# =============================================================================
# ROOT AGENT — Entry point para ADK
# =============================================================================

root_agent = LlmAgent(
    name="lia_root",
    model=config.MODELS["root"],
    description="Agente raíz de LIA V3. Recibe perspectiva y PDF, inicia pipeline de análisis.",
    instruction=ROOT_INSTRUCTION,
    global_instruction=knowledge_manager.build_global_instruction(),
    tools=[set_session_config],
    sub_agents=[pipeline],
    after_agent_callback=auto_save_report,
)
