# Contexto Legal y de Negociación — Contrato de Suministro

> **Dominio**: `contrato_suministro`
> **Normativa**: Arts. 968-980 Código de Comercio
> **Destinatarios**: Drafter, CEO

---

## Perspectiva del Análisis

**IMPORTANTE**: Adaptar TODO el análisis según la perspectiva en `session_config`.

### Si la perspectiva es "contratante" (COMPRADOR):
- Riesgos: incumplimiento del proveedor, calidad deficiente, retrasos en entregas, falta de garantías suficientes, dependencia del proveedor.
- Recomendaciones: proteger al comprador, penalidades justas, SLAs claros.
- Carta de negociación: desde comprador buscando mejores condiciones de servicio.

### Si la perspectiva es "contratista" (VENDEDOR/PROVEEDOR):
- Riesgos: multas desproporcionadas, penalidades excesivas, responsabilidad ilimitada, plazos de pago extensos, cláusulas de reemplazo unilateral, terminación sin causa justa.
- Recomendaciones: proteger al proveedor, limitar responsabilidades, asegurar pagos oportunos.
- Carta de negociación: desde proveedor buscando condiciones justas y sostenibles.

---

## Definición Legal del Dominio

Prestaciones periódicas o continuadas de bienes/servicios a cambio de contraprestación.

### Elementos Esenciales
1. **Periodicidad**: Repetición en el tiempo
2. **Plazo**: Determinado o determinable
3. **Precio**: Determinado o determinable
4. **Objeto**: Bienes o servicios específicos

---

## Principios de Redacción (para Drafter)

1. **Equilibrio**: Reciprocidad en penalidades y obligaciones.
2. **Claridad en precio**: Base + IVA + mecanismo ajuste + moneda.
3. **Protección operativa**: Protocolos claros de entrega, aceptación, rechazo.
4. **Terminación ordenada**: Preaviso mínimo 60 días, inventario pendiente.
5. **Garantías proporcionales**: 10-20% del valor anual estimado.

---

## Criterios Go/No-Go (para CEO)

| Decisión | Criterio |
|:---|:---|
| **GO** | security_score >= 80, sin CRITICAL |
| **CONDITIONAL_GO** | security_score 50-79, CRITICAL viables |
| **NO_GO** | security_score < 50, CRITICAL fatales |

### Contexto de Negocio Clave
- Competitividad del precio a largo plazo
- Garantías ante incumplimiento recurrente
- Peor escenario financiero (costo máximo)
- Top 3 cláusulas más negociables
