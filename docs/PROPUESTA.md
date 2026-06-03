# Propuesta de Investigación
## 1. Planteamiento del Problema

### Antecedentes y Contexto

El sistema de salud pública en México enfrenta una crisis estructural crónica debido a la transición epidemiológica de su población, caracterizada por una alarmante prevalencia de enfermedades crónico-degenerativas. De acuerdo con datos oficiales, México ocupa los primeros lugares a nivel mundial en obesidad, diabetes mellitus e hipertensión arterial. Esta base de vulnerabilidad metabólica se transforma en un factor crítico cuando la población interactúa con patologías respiratorias agudas (como influenza, virus sincitial respiratorio y SARS-CoV-2), las cuales se presentan de manera estacional o pandémica.

### El Problema Central

El núcleo del problema radica en la **dificultad para estratificar de manera oportuna y predictiva el riesgo de complicación clínica (hospitalización, intubación o deceso) de un paciente al momento de ingresar a los servicios de salud**.

Actualmente, los protocolos de *triage* hospitalario se basan en sintomatología inmediata y criterios lineales que, si bien son útiles, subestiman el efecto sinérgico e interactivo de las comorbilidades múltiples (multimorbilidad). Una combinación específica de factores (por ejemplo, un rango de edad intermedio sumado a tabaquismo crónico y obesidad grado I) puede presentar un riesgo de letalidad equivalente o superior al de un adulto mayor sano, pero pasa desapercibida bajo los esquemas de evaluación tradicionales.

Esta falta de herramientas analíticas avanzadas provoca dos fenómenos perjudiciales para la salud pública:

1. **Saturación innecesaria de unidades médicas:** Hospitalización preventiva de pacientes de bajo riesgo real.
2. **Altas tasas de mortalidad prevenible:** Alta hospitalaria o retraso en la atención crítica de pacientes cuya aparente estabilidad inicial enmascara un riesgo inminente de deterioro sistémico.

El sistema de salud genera millones de registros clínicos a través de la Dirección General de Epidemiología (DGE); sin embargo, este volumen masivo de información permanece subutilizado. Se le trata como un repositorio meramente estadístico e histórico, en lugar de explotarse como un activo estratégico en tiempo real.

> **Pregunta de Investigación:** ¿Cómo pueden las técnicas de minería de datos (aprendizaje supervisado y no supervisado) aplicadas a los datos históricos de la DGE identificar patrones ocultos de multimorbilidad y clasificar con precisión el riesgo de mortalidad en pacientes mexicanos, optimizando así la toma de decisiones clínicas?

## 2. Justificación Formal

### Relevancia Social y Clínica

La presente investigación se justifica por su impacto directo en la preservación de la vida humana y el bienestar social. En un país con recursos médicos, humanos y de infraestructura limitados, la capacidad de predecir con precisión matemática qué pacientes tienen mayor probabilidad de evolucionar hacia un cuadro crítico permite una asignación justa y eficiente de camas de terapia intensiva, ventiladores y personal especialista. Identificar de manera temprana los perfiles de riesgo específicos de la población mexicana es un acto de equidad en salud pública.

### Viabilidad Técnica y Valor de la Minería de Datos

El proyecto es plenamente viable debido a la disponibilidad de la base de datos abiertos de la Dirección General de Epidemiología, la cual cuenta con un volumen superior a los cientos de miles de registros individuales anonimizados y estructurados.

La metodología tradicional (como la regresión estadística simple) suele fallar al modelar interacciones complejas no lineales entre más de tres enfermedades simultáneas. Es aquí donde la **minería de datos** aporta su mayor valor:

* Algoritmos de **reglas de asociación (Apriori/FP-Growth)** permiten descubrir combinaciones de comorbilidades no intuitivas que viajan juntas en la población mexicana.
* Modelos de **clasificación (Árboles de Decisión y Random Forest)** ofrecen una ventaja única: su alta interpretabilidad. Un árbol de decisión puede traducirse directamente en un diagrama de flujo clínico que un médico general en una clínica rural puede entender y aplicar en segundos.

```
[Paciente Ingresa] ──> ¿Edad > 60? ──(Sí)──> ¿Diabetes + Obesidad? ──(Sí)──> ALTO RIESGO

```

### Impacto y Beneficios Esperados

Los resultados de este proyecto proveerán una herramienta científica para:

* **Optimización de Recursos Institucionales:** Reducir los costos operativos de instituciones como el IMSS, ISSSTE o la Secretaría de Salud mediante la reducción de hospitalizaciones innecesarias.
* **Diseño de Políticas Preventivas:** Generar alertas tempranas hiper-dirigidas hacia sectores específicos de la población (por ejemplo, campañas de vacunación prioritarias para los perfiles de comorbilidad detectados como más vulnerables).
* **Innovación Tecnológica en Salud:** Sentar las bases para el desarrollo futuro de sistemas de soporte a la decisión clínica (CDSS, por sus siglas en inglés) basados en datos reales de la población mexicana y no en modelos importados de otros países cuyas realidades demográficas son radicalmente distintas.