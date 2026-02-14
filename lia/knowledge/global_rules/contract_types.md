# Tipos de Contratos Soportados — LIA (SK-GLB-005)

> **Uso**: Inyectado al Agente INTAKE para clasificación del contrato.
> **Propósito**: ÚNICA FUENTE DE VERDAD sobre tipos de contrato, códigos y señales de clasificación.

---

## 1. Tabla de Tipos Soportados

| Código del Dominio | Nombre | Normativa Principal | Características Clave |
|:---|:---|:---|:---|
| `contrato_suministro` | Contrato de Suministro | Art. 968-980 Código de Comercio | Prestaciones periódicas o continuadas, precio determinado o determinable, plazo, cantidades |
| `contrato_laboral` | Contrato de Trabajo | Código Sustantivo del Trabajo | Subordinación, salario, prestaciones sociales, jornada laboral |
| `contrato_civil` | Contrato Civil | Código Civil (Libro IV) | Compraventa, arrendamiento, mandato, prestación de servicios, comodato |
| `contrato_general` | Contrato General / Atípico | Código Civil (Arts. 1495-1617) + Código de Comercio | **Fallback** — Se usa cuando el contrato no encaja claramente en otro tipo |

### Diferencias Clave
- **Suministro**: Prestaciones **periódicas o continuadas** en el tiempo (ej. mantenimiento mensual, aseo diario, entrega recurrente de insumos). Si hay pago mensual por servicio continuo → `contrato_suministro`.
- **Civil/Obra**: Ejecución instantánea o por entregables definidos (ej. construir una pared, pintar una fachada, entregar 1 informe).

---

## 2. Señales de Clasificación

Busca estas características en el texto completo del contrato (no solo en el encabezado):

### contrato_suministro
- Entregas periódicas o continuadas de bienes o servicios
- Precio unitario con cantidades por entrega
- Duración con periodicidad definida (mensual, trimestral, anual)
- Mención de "suministro", "abastecimiento", "provisión periódica"
- Referencia a cantidades mínimas/máximas por período

### contrato_laboral
- Relación empleador-trabajador con subordinación
- Salario fijo o variable con prestaciones sociales
- Jornada laboral definida
- Mención de "contrato de trabajo", "empleado", "trabajador", "patrono"
- Obligaciones de seguridad social (EPS, ARL, pensión)

### contrato_civil
- Compraventa de bienes (transferencia de dominio, precio, cosa)
- Arrendamiento (uso y goce de un bien, canon, plazo)
- Prestación de servicios independientes (sin subordinación)
- Mandato (encargo de gestión)
- Mención de "compraventa", "arrendamiento", "prestación de servicios", "mandato"

### contrato_general (Fallback)
- El contrato no presenta señales claras de ninguno de los tipos anteriores
- Es un contrato atípico o mixto
- El confidence_score es inferior a 0.80
- Combina características de múltiples tipos sin predominancia clara

---

## 3. Regla de Fallback

1. Si no puedes clasificar con confidence_score >= 0.80, asigna `contrato_general`.
2. Si el dominio específico no tiene archivos de Knowledge Base, el sistema usará `contrato_general` como fallback de conocimiento.
