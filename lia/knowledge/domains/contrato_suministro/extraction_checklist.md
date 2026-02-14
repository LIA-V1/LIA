# Checklist de Extracción — Contrato de Suministro

> **Dominio**: `contrato_suministro`
> **Normativa**: Arts. 968-980 Código de Comercio
> **Destinatario**: Agente Intake

---

## Elementos ESENCIALES (si falta → `status: "error"`)

1. **Identificación de las partes**: Nombre legal, NIT, representante legal, rol (suministrante/suministrado)
2. **Objeto**: Bienes o servicios a suministrar con especificaciones
3. **Precio o mecanismo de determinación**: Unitario, global, fórmula de ajuste
4. **Duración / vigencia**: Fecha inicio, fecha fin
5. **Periodicidad de las entregas**: Frecuencia (diaria, semanal, mensual, etc.)
6. **Firmas**: De ambas partes o representantes

## Elementos IMPORTANTES (si falta → `status: "warning"`)

1. Mecanismo de ajuste de precios (IPC, SMLMV, fórmula)
2. Condiciones de entrega (lugar, horario, responsabilidad en tránsito)
3. Protocolo de aceptación / rechazo de entregas
4. Pólizas y garantías
5. Cláusula de terminación anticipada

## Criterios de Evaluación

| Status | Condición |
|:---|:---|
| `"success"` | 6 esenciales completos |
| `"warning"` | Esenciales ok, pero faltan 2+ importantes |
| `"error"` | Falta al menos 1 esencial |
