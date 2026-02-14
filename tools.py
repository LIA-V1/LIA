"""
LIA V3 — Tools del Root Agent.
Tools disponibles para que el LLM interactúe con el session state.
"""
import logging
from google.adk.tools import ToolContext

logger = logging.getLogger(__name__)


def set_session_config(
    perspective: str,
    additional_context: str = "",
    tool_context: ToolContext = None,
) -> dict:
    """Guarda la configuración de sesión del usuario en el state.

    El root agent DEBE llamar esta tool antes de transferir al pipeline.
    Establece la perspectiva de análisis (contratante o contratista) y
    cualquier contexto adicional proporcionado por el usuario.

    Args:
        perspective: Perspectiva de análisis. Debe ser 'contratante' o 'contratista'.
        additional_context: Contexto adicional opcional del usuario.

    Returns:
        Confirmación con la configuración guardada.
    """
    # Normalizar perspectiva
    perspective = perspective.strip().lower()
    if perspective not in ("contratante", "contratista"):
        perspective = "contratista"  # Default seguro

    session_config = {
        "perspective": perspective,
        "additional_context": additional_context,
    }

    tool_context.state["session_config"] = session_config
    logger.info(f"✓ session_config guardado: {session_config}")

    return {
        "status": "ok",
        "message": f"Configuración guardada. Perspectiva: {perspective}.",
        "session_config": session_config,
    }
