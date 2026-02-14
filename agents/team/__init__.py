"""
LIA V3 — Team Agents.
Agentes analíticos especializados:
- Auditor: Auditoría de riesgos
- Financial: Análisis de impacto económico
- Drafter: Sugerencias de redacción + carta de negociación
- CEO: Decisión ejecutiva Go/No-Go
"""
from .auditor import auditor_agent
from .financial import financial_agent
from .drafter import drafter_agent
from .ceo import ceo_agent
