# Proyecto Final

Los detalles de la propuesta pueden verse en [Propuesta de Investigación](mds/PROPUESTA.md).

Para la organización de tareas, hitos y la asignación de roles de cada colaborador, consulta la [Guía de Desarrollo](dev-guide/README.md).

## 1. Descarga y Preparación de Datos

El proyecto cuenta con scripts automatizados para descargar y descomprimir el conjunto de datos de Influenza/COVID-19 de la Secretaría de Salud de México de forma rápida y limpia. El URL del recurso se gestiona desde [data/url.txt](data/url.txt).

### Ejecución en macOS y Linux (Bash)
Asegúrate de que el script tenga permisos de ejecución y luego córrelo desde la raíz del proyecto:
```bash
chmod +x src/scripts/download_data.sh
./src/scripts/download_data.sh [directorio_de_salida]
```
*Si no se especifica el `directorio_de_salida`, los datos se descargarán y extraerán por defecto en `data/`.*

### Ejecución en Windows (PowerShell)
Ejecuta el script desde una consola de PowerShell en la raíz del proyecto:
```powershell
.\src\scripts\download_data.ps1 -OutputDir "data"
```
*El parámetro `-OutputDir` es opcional y por defecto apunta a `data/`.*

Ambos scripts se encargan de:
1. Leer de forma limpia el URL de [data/url.txt](file:///Users/toporaku/code/dwdm/proyecto-final/data/url.txt).
2. Descargar el archivo `.zip` usando `curl` o `Invoke-WebRequest`.
3. Extraer el archivo `COVID19MEXICO.csv` directamente en la carpeta de destino (`data/`).
4. Eliminar el archivo `.zip` temporal para no ocupar espacio innecesario en disco.

---

## 2. Manual de Buenas Prácticas para Desarrolladores

Para mantener el proyecto ordenado, reproducible y listo para producción, todos los desarrolladores deben seguir las siguientes directrices estructurales:

### 2.1 Código Fuente y Utilidades (`src/`)
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

### 2.2 Serialización y Guardado de Modelos (`models/`)
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

### 2.3 Presentación en Quarto (`mds/` y `_quarto.yml`)
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

