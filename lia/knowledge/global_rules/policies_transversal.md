# Normativa Transversal Obligatoria — Aplicable a TODO Tipo de Contrato

> **Uso**: Este archivo es inyectado en el contexto de TODOS los agentes.
> **Propósito**: Verificar el cumplimiento de normas que aplican independientemente del tipo de contrato.

---

## 1. Protección de Datos Personales

### Marco Legal
- **Ley 1581 de 2012**: Ley Estatutaria de Protección de Datos Personales
- **Decreto 1377 de 2013**: Reglamentación
- **Autoridad**: Superintendencia de Industria y Comercio (SIC)

### Qué Verificar en el Contrato

| Elemento | Obligatorio | Severidad si falta |
| :--- | :--- | :--- |
| Cláusula de tratamiento de datos personales | Sí, si el contrato implica intercambio de datos | **HIGH** |
| Autorización expresa del titular de datos | Sí, si se recopilan datos de terceros | **HIGH** |
| Finalidad del tratamiento claramente definida | Sí | **MEDIUM** |
| Identificación del responsable y encargado del tratamiento | Sí | **MEDIUM** |
| Cláusula de transferencia internacional de datos | Sí, si hay transferencia cross-border | **CRITICAL** |

### Regla para los Agentes
Si el contrato involucra datos personales y NO tiene cláusula de protección de datos:
- Marcar como riesgo **HIGH**
- Citar: "Incumplimiento potencial de la Ley 1581 de 2012."

### Datos Sensibles (Protección Reforzada)
Son datos sensibles (Art. 5 Ley 1581): Origen racial, orientación política, religiosa, salud, vida sexual, biométricos.
**Si el contrato involucra datos sensibles sin autorización explícita: CRITICAL.**

---

## 2. Prevención de Lavado de Activos y Financiación del Terrorismo (AML/LAFT)

### Marco Legal
- **Ley 526 de 1999**: Creación UIAF
- **Circular Externa 100-000016 de 2020** (SAGRILAFT)

### Qué Verificar en el Contrato

| Elemento | Cuándo aplica | Severidad si falta |
| :--- | :--- | :--- |
| Cláusula de declaración de origen lícito de fondos | Contratos > 50 SMLMV o sectores regulados | **HIGH** |
| Declaración de no inclusión en listas restrictivas | Todos los contratos | **MEDIUM** |

### Regla para los Agentes
- En contratos de alto valor (> 50 SMLMV) sin cláusula de origen lícito: marcar **HIGH**.
- Alertar si el contrato involucra jurisdicciones de alto riesgo sin due diligence explícito.

---

## 3. Anticorrupción y Compliance

### Marco Legal
- **Ley 1778 de 2016**: Corrupción transnacional
- **Estatuto Anticorrupción** (Ley 1474 de 2011)

### Qué Verificar en el Contrato

| Elemento | Cuándo aplica | Severidad si falta |
| :--- | :--- | :--- |
| Cláusula anticorrupción / anti-soborno | Contratos con entidades públicas o alto valor | **HIGH** |
| Prohibición de pagos a funcionarios públicos | Contratos con trámites gubernamentales | **HIGH** |

### Regla para los Agentes
Si el contrato es con una entidad pública, la ausencia de cláusula anticorrupción es **HIGH**.

---

## 4. Facturación Electrónica

### Marco Legal
- **Decreto 358 de 2020**
- **Resolución DIAN 000042 de 2020**

### Regla para los Agentes
- Si el contrato establece pagos pero no menciona facturación electrónica: marcar **MEDIUM**.
- Si el contrato exige facturación en papel: marcar **HIGH**.

---

## 5. Cláusulas de Resolución de Conflictos

### Qué Verificar en el Contrato

| Elemento | Importancia | Severidad si falta |
| :--- | :--- | :--- |
| Mecanismo de resolución definido | Esencial | **HIGH** |
| Sede y reglas del arbitraje (si aplica) | Esencial | **MEDIUM** |
| Ley aplicable al contrato | Esencial en contratos internacionales | **CRITICAL** si es internacional |

### Regla para los Agentes
- Contrato sin cláusula de resolución de conflictos: marcar **HIGH**.
- Cláusula arbitral sin especificar centro ni reglas: marcar **MEDIUM**.

---

## 6. Régimen de Garantías y Seguros

### Qué Verificar en el Contrato

| Elemento | Cuándo aplica | Severidad si falta |
| :--- | :--- | :--- |
| Póliza de cumplimiento | Contratos > 20 SMLMV | **HIGH** |
| Cláusula penal proporcional (≤ 50% del valor) | Si hay cláusula penal | **CRITICAL** si > 50% |

### Regla para los Agentes
- Cláusula penal > 50% del valor del contrato: **CRITICAL** (posible reducción judicial).
- Contrato de valor significativo sin póliza de cumplimiento: **HIGH**.
