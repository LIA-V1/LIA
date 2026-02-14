"""
LIA V3 — Prompt Builder.
Factory de InstructionProviders para agentes del pipeline.

Cada InstructionProvider es un callable que recibe ReadonlyContext
y retorna la instrucción completa con:
1. Placeholders de state interpolados ({intake_output}, {auditor_output}, etc.)
2. Perspectiva del usuario
3. Knowledge base inyectada selectivamente según rol + dominio
"""
import logging

from .knowledge_manager import knowledge_manager

logger = logging.getLogger(__name__)

# Placeholders que se interpolan desde el state
STATE_PLACEHOLDERS = [
    "session_config",
    "intake_output",
    "auditor_output",
    "financial_output",
    "drafter_output",
    "ceo_output",
]


def create_instruction_provider(agent_name: str, base_instruction: str):
    """
    Crea un InstructionProvider dinámico para un agente.

    El provider:
    1. Interpola placeholders {key} con datos del state
    2. Lee el dominio clasificado desde state["intake_output"]
    3. Carga knowledge SELECTIVO para este agente
    4. Combina instrucción interpolada + perspectiva + knowledge

    Args:
        agent_name: Nombre/rol del agente (intake, auditor, financial, drafter, ceo)
        base_instruction: Instrucción base con placeholders opcionales

    Returns:
        Callable compatible con LlmAgent.instruction
    """
    def provider(context):
        # Obtener dominio de la clasificación del Intake
        intake_output = context.state.get("intake_output", {})

        if isinstance(intake_output, str):
            domain = "contrato_general"
        elif isinstance(intake_output, dict):
            domain = intake_output.get("contract_class", "contrato_general")
        else:
            domain = "contrato_general"

        # Obtener perspectiva
        session_config = context.state.get("session_config", {})
        if isinstance(session_config, dict):
            perspective = session_config.get("perspective", "contratista")
        else:
            perspective = "contratista"

        # Interpolar placeholders del state en la instrucción base
        interpolated = base_instruction
        for key in STATE_PLACEHOLDERS:
            placeholder = "{" + key + "}"
            if placeholder in interpolated:
                value = context.state.get(key, {})
                # Convertir a string legible (resumir si es muy largo)
                str_value = _format_state_value(key, value)
                interpolated = interpolated.replace(placeholder, str_value)

        # Obtener knowledge SELECTIVO para este agente
        agent_knowledge = knowledge_manager.get_agent_knowledge(agent_name, domain)

        full_instruction = f"""{interpolated}

## PERSPECTIVA DE ANÁLISIS: {perspective.upper()}
Analiza TODO desde la perspectiva del {perspective}.

{agent_knowledge}
"""
        logger.debug(f"[{agent_name}] Instrucción construida para dominio: {domain} "
                     f"(~{len(full_instruction)} chars)")
        return full_instruction

    return provider


def _format_state_value(key: str, value) -> str:
    """
    Formatea un valor del state para inyección en instrucciones.

    Convierte dicts/lists a representación legible sin truncar datos
    críticos que los agentes necesitan para análisis.
    """
    if value is None or value == "" or value == {}:
        return "(no disponible aún)"

    if isinstance(value, str):
        return value

    # Para dicts y lists, convertir a string
    try:
        import json
        return json.dumps(value, ensure_ascii=False, indent=2, default=str)
    except Exception:
        return str(value)
