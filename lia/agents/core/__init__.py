"""
LIA V3 — Core Agents.
Agentes fundamentales que abren y cierran el pipeline:
- Intake: Clasifica, extrae estructura y texto del PDF
- Reporter: Consolida todos los outputs en reporte final
"""
from .intake import intake_agent
from .reporter import reporter_agent
