# Guía de Desarrollo — Proyecto Final de Minería de Datos

Esta guía detalla la organización del proyecto, la asignación de responsabilidades, la arquitectura de código y los criterios de aceptación para cada entrega. Es la referencia central para todo el equipo de desarrollo.

---

## 1. Equipo y Roles

El desarrollo se divide de forma especializada en notebooks y módulos en `src/` para garantizar la modularidad y evitar conflictos en Git. La documentación y presentación es responsabilidad transversal de todo el equipo.

| Colaborador | Rol | Notebooks Asignados | Módulos `src/` Asignados |
|---|---|---|---|
| **A** | Infraestructura y Datos | `01_preprocesamiento.ipynb` | `src/data/loader.py`<br>`src/data/preprocessor.py`<br>`src/utils/constants.py` |
| **B** | Análisis Exploratorio | `02_eda.ipynb` | `src/utils/visualization.py`<br>`src/utils/association.py` |
| **C** | Modelo Supervisado | `03_modelo_supervisado.ipynb`<br>`05_demo_modelo.ipynb` | `src/models/factory.py`<br>`src/models/trainer.py`<br>`src/models/evaluator.py` |
| **D** | Clustering | `04_clustering.ipynb` | `src/models/clustering.py` |

---

## 2. Decisiones Técnicas y Arquitectura

### Variable Objetivo (`SEVERIDAD`)
Definimos una **clasificación multi-clase ordinal de severidad clínica** calculada a partir del diccionario de datos de la DGE:

| Nivel | Etiqueta | Lógica de Derivación |
|---|---|---|
| **0** | Leve (Ambulatorio) | `TIPO_PACIENTE == 1` |
| **1** | Grave (Hospitalizado) | `TIPO_PACIENTE == 2` AND `UCI != 1` AND `INTUBADO != 1` AND sin fecha de defunción |
| **2** | Crítico (UCI/Intubado) | `UCI == 1` OR `INTUBADO == 1`, sin fecha de defunción |
| **3** | Fallecido | `FECHA_DEF` válida (distinta de `9999-99-99`) |

### Estructura de Módulos (`src/`)

El código lógico está desacoplado de las celdas de Jupyter en la siguiente estructura:
```
src/
├── data/
│   ├── loader.py           → Carga, validación básica y perfiles de calidad del dataset.
│   └── preprocessor.py     → Pipeline de limpieza, codificación, imputación y creación del target.
├── models/
│   ├── factory.py          → Factory Method para Decision Tree, Random Forest y XGBoost.
│   ├── trainer.py          → Entrenamiento, validación cruzada y búsqueda de hiperparámetros.
│   ├── evaluator.py        → Métricas de evaluación, matrices de confusión y curvas ROC.
│   └── clustering.py       → K-Means, análisis jerárquico (Ward), PCA/t-SNE y perfiles.
└── utils/
    ├── constants.py        → Semillas, rutas del proyecto y listas de columnas.
    ├── visualization.py    → Funciones de graficación con estilos consistentes.
    └── association.py      → Minería de reglas de asociación con Apriori / FP-Growth.
```

---

## 3. Hitos del Proyecto (Milestones)

Todas las tareas de desarrollo deben estar completadas antes del **7 de junio de 2026**.

* **Milestone 1 (M1): Infraestructura y Preparación de Datos** (Lidera Colaborador A)
  * Implementación del preprocesamiento, extracción del target y guardado de datos limpios.
* **Milestone 2 (M2): Análisis Exploratorio de Datos** (Lidera Colaborador B)
  * Estadísticas descriptivas, detección de outliers, correlaciones y reglas de asociación.
* **Milestone 3 (M3): Modelo Supervisado** (Lidera Colaborador C)
  * Clasificación multiclase, balanceo de datos, optimización de hiperparámetros y persistencia del modelo.
* **Milestone 4 (M4): Clustering** (Lidera Colaborador D)
  * Segmentación no supervisada, justificación del número de clústeres y perfiles clínicos.
* **Milestone 5 (M5): Entregables Finales** (Todos)
  * Reporte técnico en PDF, presentación de diapositivas, vídeo expositivo y configuración de Quarto.

---

## 4. Guía de Trabajo por Issue

Para conocer los criterios de aceptación específicos de cada issue, consulta la sección de **Issues** en GitHub. Cada desarrollador debe mover sus tareas asignadas a *In Progress* y posteriormente cerrarlas mediante commits referenciando el ID del issue (ej. `fix #12`).

### Flujo de Trabajo Local
1. Instala las dependencias exactas con `uv`:
   ```bash
   uv pip install -r requirements.txt
   ```
2. Realiza el desarrollo de la lógica del módulo asignado en la carpeta `src/`.
3. Integra, ejecuta y documenta en el Jupyter Notebook asignado utilizando los módulos de `src/` importados mediante `sys.path`.
4. Renderiza localmente el sitio con Quarto para verificar la visualización:
   ```bash
   quarto preview
   ```
