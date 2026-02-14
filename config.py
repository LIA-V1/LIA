"""
LIA V3 — Configuración centralizada.
Define modelos, rutas y parámetros por defecto.

Soporta dual API keys: GOOGLE_API_KEY (flash) y GOOGLE_API_KEY_PRO (pro)
para distribuir cuotas entre dos proyectos de Google Cloud.
"""
import os
from pathlib import Path

from google.adk.models.google_llm import Gemini
from google.genai import Client, types

from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")

# =============================================================================
# RUTAS
# =============================================================================

KNOWLEDGE_DIR = BASE_DIR / "knowledge"
OUTPUT_DIR = BASE_DIR / "output"

# Crear directorio de output si no existe
OUTPUT_DIR.mkdir(exist_ok=True)

# =============================================================================
# API KEYS — Dual proyecto para distribuir cuotas
# =============================================================================

# Key principal (flash) — proyecto LIA-PROJECT
_API_KEY_FLASH = os.environ.get("GOOGLE_API_KEY", "")

# Key para modelos pro — proyecto independiente.
# Si no existe GOOGLE_API_KEY_PRO, usa la misma key (backward compatible).
_API_KEY_PRO = os.environ.get("GOOGLE_API_KEY_PRO", _API_KEY_FLASH)

# Retry automático: reintenta 503/429.  
# Usamos parámetros básicos soportados por HttpRetryOptions.
# Nota: 'multiplier' no es soportado en esta versión de google-genai.
_RETRY = types.HttpRetryOptions(initial_delay=2, attempts=3)


def _make_model(model_name: str, use_pro_key: bool = False) -> Gemini:
    """
    Crea una instancia Gemini con la API key y retry correctos.

    Utiliza inyección manual del cliente para evitar errores de validación de Pydantic
    al pasar opciones adicionales al constructor de Gemini, y para asegurar
    que se use la API key específica del proyecto (Flash o Pro).
    """
    target_key = _API_KEY_PRO if use_pro_key else _API_KEY_FLASH

    if not target_key:
        error_msg = ("GOOGLE_API_KEY_PRO" if use_pro_key else "GOOGLE_API_KEY")
        raise ValueError(f"La clave de API {error_msg} no está configurada en el entorno.")

    # 1. Instanciar Gemini de forma limpia (sin argumentos conflictivos)
    instance = Gemini(model=model_name)

    # 2. Construir y configurar el Cliente manualmente
    # Esto nos permite especificar la API key y las opciones de retry
    # bypassando las restricciones del modelo Pydantic de Gemini.
    http_options = types.HttpOptions(
        headers=instance._tracking_headers(),
        retry_options=_RETRY
    )

    client = Client(
        api_key=target_key,
        http_options=http_options
    )

    # 3. Inyectar el cliente configurado en la instancia
    # Sobreescribimos la propiedad interna para que el modelo use nuestro cliente.
    instance.__dict__["api_client"] = client

    return instance


# =============================================================================
# MODELOS POR AGENTE
# =============================================================================

MODELS = {
    "root": _make_model("gemini-2.5-flash"),
    "intake": _make_model("gemini-2.5-flash"),         # Visión nativa para PDF
    "auditor": _make_model("gemini-2.5-pro", True),    # Razonamiento profundo (Pro Key)
    "financial": _make_model("gemini-2.5-pro", True),  # Precisión numérica (Pro Key)
    "drafter": _make_model("gemini-2.5-flash"),        # Generación rápida
    "ceo": _make_model("gemini-2.5-pro", True),        # Decisión ejecutiva (Pro Key)
    "reporter": _make_model("gemini-2.5-flash"),       # Generación de reporte
}

# =============================================================================
# DEFAULTS
# =============================================================================

DEFAULT_DOMAIN = "contrato_general"
DEFAULT_PERSPECTIVE = "contratista"

# Dominios disponibles
AVAILABLE_DOMAINS = [
    "contrato_suministro",
    "contrato_general",
]

# =============================================================================
# LOGGING
# =============================================================================

# Delay entre agentes (segundos) para prevenir 503 por alta demanda.
# Solo se aplica antes de agentes que usan gemini-2.5-pro.
# Poner en 0 para desactivar.
AGENT_DELAY_SECONDS = int(os.environ.get("LIA_AGENT_DELAY", "15"))

LOG_LEVEL = os.environ.get("LIA_LOG_LEVEL", "INFO")
