"""
LIA V3 — Callbacks compartidos.
Implementan los design patterns oficiales de ADK:
- Validación de state (before_agent_callback)
- Logging estructurado (after_agent_callback)
- Persistencia de resultados (after pipeline)
"""
import json
import logging
from datetime import datetime
from pathlib import Path

from google.genai import types

from . import config

logger = logging.getLogger(__name__)


# =============================================================================
# DEPENDENCIAS DE STATE POR AGENTE
# =============================================================================

REQUIRED_STATE_KEYS = {
    "lia_auditor": ["intake_output"],
    "lia_financial": ["intake_output", "auditor_output"],
    "lia_drafter": ["intake_output", "auditor_output"],
    "lia_ceo": ["intake_output", "auditor_output", "financial_output", "drafter_output"],
    "lia_reporter": ["intake_output", "auditor_output", "financial_output", "drafter_output", "ceo_output"],
}


# =============================================================================
# 1. VALIDACIÓN — before_agent_callback
# =============================================================================

def validate_pipeline_state(callback_context, *args, **kwargs):
    """
    Valida que los datos necesarios existen en state antes de ejecutar un agente.

    Si faltan datos críticos, retorna Content con error → el agente se skipea.
    Esto previene que agentes trabajen con datos vacíos y generen garbage.

    Patrón ADK: "Conditional Skipping of Steps" via before_agent_callback.
    """
    agent_name = callback_context.agent_name
    required = REQUIRED_STATE_KEYS.get(agent_name, [])

    if not required:
        return None  # Sin requisitos, continuar normalmente

    missing = []
    for key in required:
        value = callback_context.state.get(key)
        if value is None or value == "" or value == {}:
            missing.append(key)

    if missing:
        error_msg = (
            f"⚠️ PIPELINE ERROR: El agente {agent_name} no puede ejecutarse.\n"
            f"Faltan datos en state: {missing}\n"
            f"Esto indica que un agente anterior falló o no produjo output."
        )
        logger.error(error_msg)
        return types.Content(
            parts=[types.Part.from_text(text=error_msg)]
        )

    logger.info(f"✓ [{agent_name}] Validación OK — datos requeridos presentes")
    return None  # Continuar ejecución normal


# =============================================================================
# 2. LOGGING — after_agent_callback
# =============================================================================

def log_agent_execution(callback_context, *args, **kwargs):
    """
    Registra la ejecución de cada agente con logging estructurado.

    Guarda métricas (timestamp, status) en state["_metrics"] para diagnóstico.

    Patrón ADK: "Logging and Monitoring".
    """
    agent_name = callback_context.agent_name

    # Registrar en logs
    logger.info(f"✓ [{agent_name}] Ejecución completada")

    # Guardar métricas en state
    metrics = callback_context.state.get("_metrics", {})
    if not isinstance(metrics, dict):
        metrics = {}

    metrics[agent_name] = {
        "completed_at": datetime.now().isoformat(),
        "status": "success",
    }
    callback_context.state["_metrics"] = metrics


# =============================================================================
# 3. PERSISTENCIA — auto-save después del pipeline
# =============================================================================

def auto_save_report(callback_context, *args, **kwargs):
    """
    Consolida todos los outputs del pipeline y guarda el reporte JSON final.

    Se ejecuta como after_agent_callback del SequentialAgent (pipeline completo).
    Solo guarda si todos los agentes han producido output.

    Patrón ADK: "Artifact Handling".
    """
    agent_name = callback_context.agent_name

    # Solo ejecutar para el pipeline completo, no para agentes individuales
    if agent_name != "lia_pipeline":
        return

    logger.info("📄 Consolidando reporte final...")

    try:
        state = callback_context.state

        # Recopilar todos los outputs
        report_data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "version": "LIA_V3",
            },
            "session_config": state.get("session_config", {}),
            "intake": state.get("intake_output", {}),
            "auditor": state.get("auditor_output", {}),
            "financial": state.get("financial_output", {}),
            "drafter": state.get("drafter_output", {}),
            "ceo": state.get("ceo_output", {}),
            "final_report": state.get("final_report", {}),
            "metrics": state.get("_metrics", {}),
        }

        # Guardar JSON
        config.OUTPUT_DIR.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = config.OUTPUT_DIR / f"report_{timestamp}.json"

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2, default=str)

        logger.info(f"✅ Reporte guardado: {output_path}")
        callback_context.state["_report_path"] = str(output_path)

    except Exception as e:
        logger.error(f"❌ Error guardando reporte: {e}")
        callback_context.state["_save_error"] = str(e)
