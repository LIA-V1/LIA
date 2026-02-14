"""
LIA V3 — Schemas Pydantic centralizados.
Define los output schemas de todos los agentes del pipeline.
Basado en V2 con mejoras: IntakeOutput fusiona Router+Architect,
DrafterOutput incluye carta de negociación, FinalReport consolidado.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum


# =============================================================================
# ENUMS — Valores controlados para consistencia
# =============================================================================

class AnalysisPerspective(str, Enum):
    """Perspectiva desde la cual se analiza el contrato."""
    CONTRATANTE = "contratante"
    CONTRATISTA = "contratista"


class SeverityLevel(str, Enum):
    """Niveles de severidad estandarizados."""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class ActionRecommended(str, Enum):
    """Acciones recomendadas estandarizadas."""
    MODIFICAR = "MODIFICAR"
    ELIMINAR = "ELIMINAR"
    MANTENER = "MANTENER"
    AGREGAR = "AGREGAR"


class GoNoGoDecision(str, Enum):
    """Decisión ejecutiva Go/No-Go."""
    GO = "GO"
    CONDITIONAL_GO = "CONDITIONAL_GO"
    NO_GO = "NO_GO"


# =============================================================================
# SESSION CONFIG
# =============================================================================

class SessionConfig(BaseModel):
    """Configuración de sesión proporcionada por el usuario."""
    perspective: AnalysisPerspective = Field(
        ...,
        description="Perspectiva de análisis: 'contratante' o 'contratista'"
    )
    additional_context: str = Field(
        default="",
        description="Contexto adicional sobre la situación del usuario"
    )


# =============================================================================
# INTAKE OUTPUT (fusiona Router + Architect de V2)
# =============================================================================

class ContractParty(BaseModel):
    """Parte contractual identificada."""
    role: str = Field(..., description="Rol: CONTRATANTE o CONTRATISTA")
    name: str = Field(..., description="Nombre legal completo")
    identifier: str = Field(default="", description="NIT o documento de identificación")
    representative: str = Field(default="", description="Representante legal")


class ContractDates(BaseModel):
    """Fechas relevantes del contrato."""
    signing_date: str = Field(default="", description="Fecha de firma ISO 8601")
    start_date: str = Field(default="", description="Fecha de inicio ISO 8601")
    end_date: str = Field(default="", description="Fecha de finalización ISO 8601")


class StructuralElement(BaseModel):
    """Elemento estructural del contrato."""
    element_id: str = Field(..., description="Identificador único")
    element_name: str = Field(..., description="Nombre del elemento")
    is_essential: bool = Field(..., description="Si es esencial para validez")
    present: bool = Field(..., description="Si está presente en el contrato")
    location: str = Field(default="", description="Ubicación (cláusula, página)")
    observation: str = Field(default="", description="Observación")


class IntakeOutput(BaseModel):
    """
    Output del Intake Agent — Fusiona Router + Architect de V2.
    Clasifica el contrato Y extrae su estructura completa.
    """
    # Clasificación (ex-Router)
    contract_class: str = Field(
        ...,
        description="Código de clasificación: 'contrato_suministro', 'contrato_general', etc."
    )
    confidence_score: float = Field(
        ...,
        description="Confianza de clasificación entre 0.0 y 1.0"
    )
    detected_signals: List[str] = Field(
        default_factory=list,
        description="Keywords o cláusulas que justifican la clasificación"
    )
    classification_reasoning: str = Field(
        ...,
        description="Explicación de por qué se eligió esta clasificación"
    )

    # Estructura (ex-Architect)
    contract_name: str = Field(..., description="Nombre o título del contrato")
    contract_id: str = Field(default="", description="Número o código del contrato")
    parties: List[ContractParty] = Field(default_factory=list, description="Partes del contrato")
    dates: ContractDates = Field(default_factory=ContractDates, description="Fechas del contrato")
    object_description: str = Field(..., description="Objeto del contrato")
    total_value: float = Field(default=0.0, description="Valor total del contrato")
    currency: str = Field(default="COP", description="Moneda del contrato")
    duration: str = Field(default="", description="Duración del contrato")
    governing_law: str = Field(default="", description="Ley aplicable")
    jurisdiction: str = Field(default="", description="Jurisdicción")
    structural_elements: List[StructuralElement] = Field(
        default_factory=list,
        description="Elementos estructurales evaluados"
    )

    # contract_text ELIMINADO — el Auditor lee el PDF directamente.
    # Mantener el texto completo consumía tokens excesivos al propagarse
    # via {intake_output} a todos los agentes del pipeline.
    summary: str = Field(
        ...,
        description="Resumen ejecutivo del análisis estructural"
    )


# =============================================================================
# AUDITOR OUTPUT
# =============================================================================

class RiskFinding(BaseModel):
    """Hallazgo de riesgo individual."""
    risk_id: str = Field(..., description="Código del riesgo (ej: R-PRICE-001)")
    category: str = Field(..., description="Categoría (ej: Regulatorio, Financiero)")
    severity: SeverityLevel = Field(..., description="Nivel de severidad")
    clause_reference: str = Field(..., description="Referencia a la cláusula")
    original_text: str = Field(default="", description="Texto original problemático")
    description: str = Field(..., description="Descripción clara del hallazgo")
    implication: str = Field(..., description="Impacto potencial del riesgo")
    economic_impact: float = Field(default=0.0, description="Impacto económico estimado COP")
    recommendation: str = Field(..., description="Recomendación de mitigación")
    action: ActionRecommended = Field(
        default=ActionRecommended.MODIFICAR,
        description="Acción recomendada"
    )


class AuditorOutput(BaseModel):
    """Output del Auditor — Auditoría de riesgos del contrato."""
    summary: str = Field(..., description="Resumen ejecutivo de la auditoría")
    total_findings: int = Field(..., description="Número total de hallazgos")
    critical_count: int = Field(default=0, description="Hallazgos CRITICAL")
    high_count: int = Field(default=0, description="Hallazgos HIGH")
    medium_count: int = Field(default=0, description="Hallazgos MEDIUM")
    low_count: int = Field(default=0, description="Hallazgos LOW")
    findings: List[RiskFinding] = Field(
        default_factory=list,
        description="Lista de hallazgos de riesgo"
    )


# =============================================================================
# FINANCIAL OUTPUT
# =============================================================================

class FinancialRiskItem(BaseModel):
    """Item individual de riesgo financiero."""
    concept: str = Field(..., description="Concepto del riesgo financiero")
    estimated_amount: float = Field(default=0.0, description="Monto estimado COP")
    percentage_of_contract: float = Field(default=0.0, description="% respecto al valor total")
    explanation: str = Field(..., description="Explicación del cálculo")


class FinancialOutput(BaseModel):
    """Output del Financial — Análisis de impacto económico."""
    summary: str = Field(..., description="Resumen del análisis financiero")
    contract_value: float = Field(..., description="Valor total del contrato COP")
    currency: str = Field(default="COP", description="Moneda")
    payment_terms: str = Field(default="", description="Términos de pago")
    total_estimated_risk: float = Field(default=0.0, description="Riesgo económico total COP")
    potential_savings: float = Field(default=0.0, description="Ahorro potencial si se negocia")
    net_risk_after_mitigation: float = Field(default=0.0, description="Riesgo neto post-mitigación")
    risk_breakdown: List[FinancialRiskItem] = Field(
        default_factory=list,
        description="Desglose de riesgos financieros"
    )


# =============================================================================
# DRAFTER OUTPUT
# =============================================================================

class DraftingSuggestion(BaseModel):
    """Sugerencia de redacción para una cláusula."""
    clause_reference: str = Field(..., description="Referencia a la cláusula")
    original_text: str = Field(..., description="Texto original")
    identified_issue: str = Field(..., description="Problema identificado")
    suggested_redraft: str = Field(..., description="Propuesta de nueva redacción")
    justification: str = Field(..., description="Justificación legal")


class DrafterOutput(BaseModel):
    """Output del Drafter — Sugerencias de redacción + carta de negociación."""
    summary: str = Field(..., description="Resumen de las sugerencias")
    total_suggestions: int = Field(..., description="Número total de sugerencias")
    suggestions: List[DraftingSuggestion] = Field(
        default_factory=list,
        description="Lista de sugerencias de redacción"
    )
    negotiation_letter: str = Field(
        default="",
        description="Carta modelo de negociación basada en los hallazgos"
    )


# =============================================================================
# CEO OUTPUT
# =============================================================================

class CeoOutput(BaseModel):
    """Output del CEO — Visión ejecutiva y decisión Go/No-Go."""
    decision: GoNoGoDecision = Field(..., description="Decisión Go/No-Go")
    security_score: int = Field(..., description="Puntaje de seguridad 0-100")
    executive_summary: str = Field(..., description="Resumen para alta dirección")
    main_concerns: List[str] = Field(
        default_factory=list,
        description="Principales preocupaciones (max 5)"
    )
    recommendation: str = Field(..., description="Recomendación estratégica detallada")
    conditions_for_approval: List[str] = Field(
        default_factory=list,
        description="Condiciones antes de firmar (si aplica)"
    )
    decision_rationale: str = Field(
        default="",
        description="Razonamiento detallado de la decisión"
    )


# =============================================================================
# FINAL REPORT (consolidado)
# =============================================================================

class FinalReport(BaseModel):
    """
    Schema consolidado del reporte final.
    Recopila outputs de todos los agentes en un solo documento.
    """
    # Metadata
    perspective: str = Field(..., description="Perspectiva del análisis")
    contract_name: str = Field(..., description="Nombre del contrato")
    contract_class: str = Field(..., description="Clasificación del dominio")
    confidence_score: float = Field(..., description="Score de confianza")

    # Datos estructurales (del Intake)
    parties: List[ContractParty] = Field(default_factory=list)
    dates: ContractDates = Field(default_factory=ContractDates)
    contract_value: float = Field(default=0.0)
    currency: str = Field(default="COP")
    duration: str = Field(default="")
    object_description: str = Field(default="")

    # Decisión ejecutiva (del CEO)
    executive_summary: str = Field(...)
    decision: GoNoGoDecision = Field(...)
    security_score: int = Field(...)
    recommendation: str = Field(...)

    # Hallazgos (del Auditor)
    findings: List[RiskFinding] = Field(default_factory=list)

    # Análisis financiero (del Financial)
    financial_analysis: Optional[FinancialOutput] = Field(default=None)

    # Sugerencias de redacción (del Drafter)
    drafting_suggestions: List[DraftingSuggestion] = Field(default_factory=list)
    negotiation_letter: str = Field(default="")

    # Reporte Markdown
    markdown_report: str = Field(
        default="",
        description="Reporte completo en formato Markdown"
    )
