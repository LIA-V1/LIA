# Contexto Legal y de Negociación — Contrato General / Atípico

> **Dominio**: `contrato_general`
> **Destinatarios**: Drafter, CEO

---

## Perspectiva del Análisis

**IMPORTANTE**: Adaptar TODO el análisis según la perspectiva en `session_config`.

### Si la perspectiva es "contratante" (COMPRADOR):
- Riesgos: incumplimiento de la contraparte, objeto indeterminado, falta de garantías, desequilibrio a favor de la contraparte.
- Recomendaciones: proteger al comprador, asegurar cumplimiento, penalidades efectivas.
- Carta de negociación: desde la posición del comprador.

### Si la perspectiva es "contratista" (VENDEDOR/PROVEEDOR):
- Riesgos: cláusulas leoninas, responsabilidad ilimitada, penalidades desproporcionadas, terminación unilateral sin causa, plazos de pago excesivos.
- Recomendaciones: proteger al proveedor, limitar exposición, equilibrar obligaciones.
- Carta de negociación: desde la posición del proveedor.

---

## Principios Legales del Dominio

1. **Autonomía de la voluntad** (Art. 1602 C.C.)
2. **Buena fe** (Art. 1603 C.C.)
3. **Enriquecimiento sin causa**
4. **Abuso del derecho**

### Elementos de Validez (Art. 1502 C.C.)
1. Capacidad legal
2. Consentimiento libre de vicios
3. Objeto lícito
4. Causa lícita

---

## Principios de Redacción (para Drafter)

1. **Claridad absoluta**: Legal Design — si necesita abogado para entenderse, reescribir.
2. **Reciprocidad**: Cargas equilibradas entre las partes.
3. **Completitud**: Qué, quién, cuándo, cómo, con qué consecuencias.
4. **Protección sin abuso**: Cláusulas protectoras que no sean leoninas.

---

## Criterios Go/No-Go (para CEO)

| Decisión | Criterio |
|:---|:---|
| **GO** | security_score >= 80, sin hallazgos CRITICAL |
| **CONDITIONAL_GO** | security_score 50-79, CRITICAL corregibles con negociación |
| **NO_GO** | security_score < 50, CRITICAL fatales o irresolubles |

### Preguntas Clave de Negocio
- ¿El contrato es jurídicamente válido?
- ¿Las obligaciones están equilibradas?
- ¿Los riesgos financieros son aceptables?
- ¿Qué puntos concretos se deben negociar?
