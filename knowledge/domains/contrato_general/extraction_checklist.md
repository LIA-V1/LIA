# Checklist de Extracción — Contrato General / Atípico (Fallback)

> **Dominio**: `contrato_general`
> **Destinatario**: Agente Intake
> **Propósito**: Definir qué campos extraer y cómo evaluar la completitud estructural.

---

## Elementos ESENCIALES (si falta → `status: "error"`)

1. **Identificación de las partes**: Nombre legal, NIT/CC, representante legal, capacidad
2. **Objeto del contrato**: Descripción clara de las prestaciones
3. **Contraprestación**: Precio, valor o forma de pago
4. **Duración / vigencia**: Fecha inicio, fecha fin o plazo
5. **Firmas**: Al menos de las partes o sus representantes

## Elementos IMPORTANTES (si falta → `status: "warning"`)

1. Cláusula de terminación (causales, preaviso)
2. Cláusula penal (monto, porcentaje)
3. Ley aplicable y jurisdicción
4. Garantías (pólizas, avales)

## Criterios de Evaluación

| Status | Condición |
|:---|:---|
| `"success"` | 5 esenciales completos |
| `"warning"` | Esenciales ok, pero faltan 2+ importantes |
| `"error"` | Falta al menos 1 esencial |
