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

---

## 5. Manual de Buenas Prácticas para Desarrolladores

Para mantener el proyecto ordenado, reproducible y listo para producción, todos los desarrolladores deben seguir las siguientes directrices estructurales:

### 5.1 Código Fuente y Utilidades (`src/`)
**Regla:** Queda estrictamente prohibido definir funciones auxiliares complejas, algoritmos de minería de datos, utilidades de carga de datos o funciones de preprocesamiento directamente en las celdas de los notebooks. Todo este código debe residir en la carpeta `src/` (por capas correspondientes: `data/`, `models/`, `utils/`).

#### Cómo importar y referenciar utilidades en los Jupyter Notebooks:
Debido a que los notebooks están localizados en la carpeta `notebooks/`, se debe añadir la raíz del proyecto al `sys.path` antes de importar módulos de `src`.

Ejemplo de cabecera para un notebook (`notebooks/01_preprocesamiento.ipynb` o similares):
```python
import sys
from pathlib import Path

# Añadir la raíz del proyecto al path
project_root = Path.cwd().parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

# Ahora es posible importar de forma limpia desde la carpeta src
from src.data.loader import DataLoader
from src.data.preprocessor import DataPreprocessor
from src.utils.constants import RANDOM_STATE
```

---

### 5.2 Serialización y Guardado de Modelos (`models/`)
**Regla:** Los modelos entrenados en los notebooks (árboles de decisión, random forest, xgboost, etc.) no deben re-entrenarse cada vez que se ejecute la visualización, la demo o la generación de reportes. Estos deben ser serializados en la carpeta `models/`.

#### Cómo serializar modelos en un Jupyter Notebook:
Se recomienda usar la librería `joblib` para modelos de Scikit-Learn y XGBoost.

##### Ejemplo de guardado (Serialización):
```python
import joblib
from pathlib import Path

# Instanciar y entrenar el modelo (usando la factoría)
from src.models.factory import ModelFactory
model = ModelFactory.create_model("random_forest", n_estimators=100)
model.fit(X_train, y_train)

# Definir la ruta de guardado en la carpeta models/
models_dir = Path.cwd().parent / "models"
models_dir.mkdir(exist_ok=True)
model_path = models_dir / "random_forest.joblib"

# Guardar el modelo en disco
joblib.dump(model, model_path)
print(f"Modelo guardado exitosamente en: {model_path}")
```

##### Ejemplo de carga (Deserialización en `notebooks/05_demo_modelo.ipynb`):
```python
import joblib
from pathlib import Path

# Ruta del modelo
model_path = Path.cwd().parent / "models" / "random_forest.joblib"

# Cargar el modelo guardado
loaded_model = joblib.load(model_path)

# Usar el modelo cargado para realizar predicciones con nuevos datos
predictions = loaded_model.predict(X_new)
```

---

### 5.3 Presentación en Quarto (`mds/` y `_quarto.yml`)
**Regla:** La visualización del reporte técnico y de las páginas del sitio web se realiza con Quarto. El código fuente y páginas estáticas residen en `mds/` (como `index.qmd` y `about.qmd`), mientras que los notebooks en `notebooks/` se renderizan de forma integrada o mediante shortcodes de Quarto.

#### A. Renderizado directo de Notebooks en la Web de Quarto
Los notebooks están enlazados en el menú de navegación dentro de `_quarto.yml`.

Ejemplo de configuración en `_quarto.yml`:
```yaml
website:
  title: "Minería de Datos - COVID19/Influenza"
  navbar:
    left:
      - href: mds/index.qmd
        text: "Inicio"
      - href: notebooks/01_preprocesamiento.ipynb
        text: "Preprocesamiento"
      - href: notebooks/02_eda.ipynb
        text: "EDA"
```

#### B. Embeber celdas utilizando el shortcode `embed`
Quarto permite incrustar gráficos, tablas y métricas calculadas en un notebook dentro de un archivo `.qmd` usando `{{< embed >}}`.

##### Ejemplo de archivo `.qmd` (`mds/index.qmd`):
```markdown
## Resultados de la Clasificación

A continuación se muestra la curva ROC generada en el notebook de modelado:

{{< embed ../notebooks/03_modelo_supervisado.ipynb#fig-curva-roc >}}
```

##### Requisitos para el embedding en Quarto:
1. El notebook de origen debe tener declaradas las celdas referenciables agregando el tag al principio de la celda de código:
   ```python
   #| label: fig-curva-roc
   #| fig-cap: "Curva ROC de la clasificación de severidad."
   # (Tu código de graficación aquí)
   ```
2. Recuerda que para ejecutar las compilaciones locales se debe usar `quarto render` o `quarto preview`.
