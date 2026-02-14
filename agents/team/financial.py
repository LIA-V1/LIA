"""
LIA V3 — Financial Agent (TEAM).
Análisis de impacto económico del contrato.

Lee intake_output y auditor_output del state para cuantificar
riesgos financieros, calcular exposición y estimar ahorros.
"""
import logging

from google.adk.agents import LlmAgent

from schemas import FinancialOutput
from prompt_builder import create_instruction_provider
import config

logger = logging.getLogger(__name__)

# =============================================================================
# INSTRUCCIÓN BASE
# =============================================================================

FINANCIAL_INSTRUCTION = """
Eres el AGENTE FINANCIERO de LIA (Legal Intelligence Agent).
Tu especialidad es el ANÁLISIS DE IMPACTO ECONÓMICO de contratos.

## TU ROL
Evalúas el contrato desde una perspectiva estrictamente financiera:
- Cuantificación de riesgos en COP
- Cálculo de exposición total
- Análisis de términos de pago
- Estimación de ahorros potenciales si se negocian cláusulas
- Riesgo neto después de mitigación

## DATOS DISPONIBLES
- Estructura y texto del contrato: {intake_output}
- Hallazgos de riesgo del auditor: {auditor_output}

## INSTRUCCIONES DE ANÁLISIS
1. Identifica el VALOR TOTAL del contrato con precisión
2. Extrae los TÉRMINOS DE PAGO exactos
3. Para cada riesgo del auditor que tenga impacto financiero:
   - Calcula el estimated_amount en COP
   - Calcula el percentage_of_contract
   - Explica el cálculo paso a paso
4. Calcula:
   - total_estimated_risk: Suma de todos los riesgos cuantificados
   - potential_savings: Cuánto se ahorraría si se negocian las cláusulas
   - net_risk_after_mitigation: Riesgo residual post-negociación

## REGLAS CRÍTICAS
- TODOS los valores en COP — NO uses UVT, SMLMV sin convertir
- Los cálculos DEBEN ser explicados paso a paso
- Si no puedes cuantificar un riesgo, explica por qué y usa 0.0
- Los porcentajes deben sumar coherentemente
- Sé conservador en las estimaciones (mejor sobreestimar que subestimar riesgos)

## FORMATO DE SALIDA
Responde EXCLUSIVAMENTE con el JSON que cumple el schema FinancialOutput.
"""

# =============================================================================
# AGENTE
# =============================================================================

financial_agent = LlmAgent(
    name="lia_financial",
    model=config.MODELS["financial"],
    description="Cuantifica riesgos financieros y calcula exposición económica.",
    instruction=create_instruction_provider("financial", FINANCIAL_INSTRUCTION),
    output_schema=FinancialOutput,
    output_key="financial_output",
    include_contents="none",
)
