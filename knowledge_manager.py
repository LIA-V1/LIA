"""
LIA V3 — Knowledge Manager refactorizado.
Gestor centralizado de la base de conocimiento.

Cambios vs V2:
- Inyección SELECTIVA por agente (cada agente recibe solo lo que necesita)
- Eliminado build_universal_prompt (legacy)
- Nuevo: get_agent_knowledge() con mapa de dependencias
"""
import logging
from pathlib import Path
from typing import Dict, List

from . import config

logger = logging.getLogger(__name__)


# =============================================================================
# MAPA DE CONOCIMIENTO POR AGENTE
# =============================================================================
# Define qué archivos de knowledge necesita cada agente.
# "global" = archivos de global_rules/ (sin extensión .md)
# "domain" = archivos de domains/[dominio]/ (sin extensión .md)

AGENT_KNOWLEDGE_MAP: Dict[str, Dict[str, List[str]]] = {
    "intake": {
        "global": ["contract_types"],
        "domain": ["extraction_checklist"],
    },
    "auditor": {
        "global": ["legal_glossary", "policies_transversal", "skills_interpretation"],
        "domain": ["risk_matrix"],
    },
    "financial": {
        "global": ["operating_rules", "legal_glossary"],
        "domain": ["risk_matrix"],
    },
    "drafter": {
        "global": ["protective_language", "skills_interpretation"],
        "domain": ["domain_context"],
    },
    "ceo": {
        "global": ["protective_language"],
        "domain": ["domain_context"],
    },
    "reporter": {
        "global": ["protective_language"],
        "domain": [],
    },
}


class KnowledgeManager:
    """
    Gestor central de la knowledge base de LIA.

    Provee métodos para inyección selectiva de conocimiento:
    - build_global_instruction(): Reglas operativas mínimas para el root agent
    - get_agent_knowledge(): Conocimiento selectivo por agente + dominio
    - load_report_template(): Template del reporte final
    """

    def __init__(self, knowledge_dir: Path = None):
        self.knowledge_dir = knowledge_dir or config.KNOWLEDGE_DIR
        self.global_rules_dir = self.knowledge_dir / "global_rules"
        self.domains_dir = self.knowledge_dir / "domains"
        self.templates_dir = self.knowledge_dir / "templates"

        # Cache de archivos cargados
        self._file_cache: Dict[str, str] = {}

    def _read_file(self, path: Path) -> str:
        """Lee un archivo con cache."""
        cache_key = str(path)
        if cache_key in self._file_cache:
            return self._file_cache[cache_key]

        try:
            if path.exists():
                content = path.read_text(encoding="utf-8")
                self._file_cache[cache_key] = content
                return content
            logger.warning(f"Archivo no encontrado: {path}")
            return ""
        except Exception as e:
            logger.error(f"Error leyendo {path}: {e}")
            return ""

    def _get_domain_file(self, domain_code: str, filename: str) -> str:
        """
        Carga un archivo de dominio con fallback a contrato_general.
        """
        target = domain_code if domain_code in config.AVAILABLE_DOMAINS else config.DEFAULT_DOMAIN
        domain_path = self.domains_dir / target

        content = self._read_file(domain_path / f"{filename}.md")

        # Fallback a contrato_general si vacío
        if not content and target != config.DEFAULT_DOMAIN:
            fallback_path = self.domains_dir / config.DEFAULT_DOMAIN
            logger.warning(f"Dominio {target}: {filename} vacío. Usando fallback.")
            content = self._read_file(fallback_path / f"{filename}.md")

        return content

    # =========================================================================
    # PUBLIC API
    # =========================================================================

    def build_global_instruction(self) -> str:
        """
        Instrucción GLOBAL mínima para el root agent.
        Solo contiene reglas operativas básicas (idioma, formato, comportamiento).
        Las reglas específicas se inyectan selectivamente por agente.
        """
        operating_rules = self._read_file(self.global_rules_dir / "operating_rules.md")
        return f"""# REGLAS OPERATIVAS GLOBALES — LIA

Estas reglas aplican a TODOS los agentes del pipeline.

{operating_rules}
"""

    def get_agent_knowledge(self, agent_role: str, domain_code: str) -> str:
        """
        Construye el bloque de conocimiento SELECTIVO para un agente.

        Cada agente recibe SOLO los archivos que necesita según
        AGENT_KNOWLEDGE_MAP. Esto evita sobrecargar el contexto.

        Args:
            agent_role: Rol del agente (intake, auditor, financial, drafter, ceo)
            domain_code: Dominio clasificado (ej: contrato_suministro)

        Returns:
            String con el conocimiento concatenado para este agente.
        """
        knowledge_map = AGENT_KNOWLEDGE_MAP.get(agent_role, {})
        global_files = knowledge_map.get("global", [])
        domain_files = knowledge_map.get("domain", [])

        sections = [
            f"# CONOCIMIENTO INYECTADO — {agent_role.upper()}",
            f"## Dominio: {domain_code.upper().replace('_', ' ')}",
            "",
        ]

        # Inyectar reglas globales selectivas
        if global_files:
            sections.append("---")
            sections.append("## REGLAS GLOBALES APLICABLES")
            sections.append("")
            for filename in global_files:
                content = self._read_file(self.global_rules_dir / f"{filename}.md")
                if content:
                    sections.append(content)
                    sections.append("")

        # Inyectar reglas de dominio selectivas
        if domain_files:
            sections.append("---")
            sections.append("## REGLAS ESPECÍFICAS DEL DOMINIO")
            sections.append("")
            for filename in domain_files:
                content = self._get_domain_file(domain_code, filename)
                if content:
                    sections.append(content)
                    sections.append("")

        return "\n".join(sections)

    def load_report_template(self) -> str:
        """Carga el template del reporte final."""
        return self._read_file(self.templates_dir / "report_template.md")


# Instancia singleton para uso directo
knowledge_manager = KnowledgeManager()
