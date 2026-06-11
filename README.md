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

## 2. Instalación y Ejecución del Proyecto

Sigue estos pasos para configurar y ejecutar el proyecto en tu entorno local:

### 2.1 Requisitos Previos

- **Python**: Versión 3.10 o superior.
- **Quarto**: Opcional, necesario únicamente si deseas compilar o previsualizar el sitio web localmente.

### 2.2 Configuración del Entorno

1. **Clonar el repositorio:**
   ```bash
   git clone <url-del-repositorio>
   cd proyecto-final
   ```

2. **Crear y activar un entorno virtual:**
   - En macOS y Linux:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - En Windows:
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```

3. **Instalar dependencias:**
   - Usando `pip` estándar:
     ```bash
     pip install -r requirements.txt
     ```
   - Usando `uv` (recomendado por velocidad):
     ```bash
     uv pip install -r requirements.txt
     ```

---

### 2.3 Modelos en Hugging Face (Importante)

Para evitar entrenar los modelos pesados desde cero en cada ejecución, el proyecto utiliza modelos serializados pre-entrenados (Decision Tree, Random Forest y XGBoost). 

> [!IMPORTANT]
> **Alojamiento en Hugging Face:**
> Todos los modelos serializados (`.joblib`) están publicados en el siguiente repositorio de Hugging Face:
> [Hugging Face — covid19mexico-models](https://huggingface.co/toporaku/covid19mexico-models)
> 
> La URL de descarga se gestiona desde [models/url.txt](models/url.txt).

**Carga automática:**
El notebook [05_demo_modelo.ipynb](notebooks/05_demo_modelo.ipynb) y el código del pipeline de inferencia están diseñados para verificar si los modelos existen localmente en la carpeta `models/`. Si no existen, **se descargarán automáticamente** desde Hugging Face usando la URL base configurada.

---

### 2.4 Ejecución de Notebooks y Código

Para explorar el análisis y correr los modelos:

1. Inicia Jupyter Lab o Notebook:
   ```bash
   jupyter lab
   ```
2. Abre y ejecuta los notebooks en orden secuencial dentro de la carpeta `notebooks/`.

---

### 2.5 Compilación de la Documentación (Quarto)

Para previsualizar localmente el sitio de Quarto con toda la documentación y reportes integrados:

```bash
quarto preview
```

Para generar la versión estática de producción en la carpeta `docs/`:

```bash
quarto render
```


