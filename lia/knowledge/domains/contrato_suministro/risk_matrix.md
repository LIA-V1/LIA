# Matriz de Riesgos — Contrato de Suministro

> **Dominio**: `contrato_suministro`
> **Uso**: Inyectado para el Auditor.

## Riesgos de Precio y Condiciones Financieras

### R-PRICE-001: Cláusula Penal Desproporcionada
- **Severidad**: CRITICAL
- **Indicador**: >50% valor contrato; sobre valor total (no incumplido).
- **Umbral**: CRITICAL >50%; HIGH 30-50%.

### R-PRICE-002: Precio sin Mecanismo de Ajuste
- **Severidad**: HIGH
- **Indicador**: Fijo >12 meses sin IPC/Revisión.
- **Impacto**: Erosión margen.

### R-PRICE-003: Moneda Extranjera sin Cobertura
- **Severidad**: HIGH
- **Indicador**: USD/EUR sin tasa cambio/cobertura.

### R-PRICE-004: Impuestos no Definidos
- **Severidad**: MEDIUM
- **Indicador**: Ambigüedad en IVA/Retención.

---

## Riesgos de Cumplimiento y Garantías

### R-COMP-001: Ausencia Póliza Cumplimiento
- **Severidad**: HIGH
- **Indicador**: Sin póliza/garantía >20 SMLMV.

### R-COMP-002: Plazos Entrega Ambiguos
- **Severidad**: MEDIUM
- **Indicador**: "A la brevedad", sin cronograma.

### R-COMP-003: Cantidades Indeterminadas
- **Severidad**: MEDIUM
- **Indicador**: Sin mínimos/máximos claros.

### R-COMP-004: Garantía Calidad Insuficiente
- **Severidad**: MEDIUM
- **Indicador**: Sin especificaciones/plazo garantía.

---

## Riesgos de Terminación y Continuidad

### R-TERM-001: Renovación Automática sin Límite
- **Severidad**: HIGH
- **Indicador**: Sin opt-out o límite renovaciones.

### R-TERM-002: Terminación Unilateral Asimétrica
- **Severidad**: HIGH
- **Indicador**: Solo una parte puede terminar; preaviso desigual.

### R-TERM-003: Costos Terminación Excesivos
- **Severidad**: HIGH
- **Indicador**: Penalidad >30% valor restante; lucro cesante futuro.

---

## Riesgos Regulatorios

### R-REG-001: Sin Cláusula Datos Personales
- **Severidad**: HIGH
- **Indicador**: Hay datos sin cláusula/autorización.

### R-REG-002: Sin Origen Lícito (LAFT)
- **Severidad**: HIGH
- **Indicador**: >50 SMLMV sin cláusula LAFT.

### R-REG-003: Sin Resolución Conflictos
- **Severidad**: HIGH
- **Indicador**: Ausente o ambigua.

---

## Riesgos Operativos

### R-OPS-001: Responsabilidad Ilimitada
- **Severidad**: HIGH
- **Indicador**: Sin tope (cap) de responsabilidad.

### R-OPS-002: Fuerza Mayor Mal Definida
- **Severidad**: MEDIUM
- **Indicador**: Lista cerrada, excluye pandemias.

### R-OPS-003: Subcontratación sin Control
- **Severidad**: MEDIUM
- **Indicador**: Permitida sin aval previo.
