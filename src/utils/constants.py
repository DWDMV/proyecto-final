"""
Constantes globales del proyecto.

Centraliza semillas de reproducibilidad, rutas del proyecto,
listas de columnas por tipo y mapeos del diccionario de datos.

Colaborador responsable: A (Infraestructura y Datos)
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# Reproducibilidad
# ---------------------------------------------------------------------------
RANDOM_STATE: int = 42

# ---------------------------------------------------------------------------
# Rutas del proyecto (relativas a la raíz del repositorio)
# ---------------------------------------------------------------------------
PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]

DATA_RAW_PATH: Path = PROJECT_ROOT / "data_raw"
DATA_CLEAN_PATH: Path = PROJECT_ROOT / "data"
MODELS_PATH: Path = PROJECT_ROOT / "models"
REPORTS_PATH: Path = PROJECT_ROOT / "reports"
DIAGRAMS_PATH: Path = PROJECT_ROOT / "diagrams"

CSV_FILENAME: str = "COVID19MEXICO.csv"

# ---------------------------------------------------------------------------
# Columnas del dataset
# ---------------------------------------------------------------------------

# Variables de comorbilidad (binarias: 1=Sí, 2=No, 97/98/99=especial)
COLS_COMORBILIDADES: list[str] = [
    "DIABETES",
    "EPOC",
    "ASMA",
    "INMUSUPR",
    "HIPERTENSION",
    "OTRA_COM",
    "CARDIOVASCULAR",
    "OBESIDAD",
    "RENAL_CRONICA",
    "TABAQUISMO",
]

# Variables demográficas
COLS_DEMOGRAFICAS: list[str] = [
    "EDAD",
    "SEXO",
    "ENTIDAD_RES",
    "NACIONALIDAD",
    "EMBARAZO",
    "HABLA_LENGUA_INDIG",
    "INDIGENA",
]

# Variables de desenlace clínico (usadas para derivar SEVERIDAD)
COLS_DESENLACE: list[str] = [
    "TIPO_PACIENTE",
    "INTUBADO",
    "UCI",
    "FECHA_DEF",
    "NEUMONIA",
]

# Variables de diagnóstico / laboratorio
COLS_DIAGNOSTICO: list[str] = [
    "TOMA_MUESTRA_LAB",
    "RESULTADO_PCR",
    "RESULTADO_PCR_COINFECCION",
    "TOMA_MUESTRA_ANTIGENO",
    "RESULTADO_ANTIGENO",
    "CLASIFICACION_FINAL_COVID",
    "CLASIFICACION_FINAL_FLU",
]

# Variables de fechas
COLS_FECHAS: list[str] = [
    "FECHA_ACTUALIZACION",
    "FECHA_INGRESO",
    "FECHA_SINTOMAS",
    "FECHA_DEF",
]

# Variable objetivo
TARGET_COL: str = "SEVERIDAD"

# ---------------------------------------------------------------------------
# Mapeos del diccionario de datos
# ---------------------------------------------------------------------------

# Códigos especiales que representan datos faltantes o no aplicables
CODIGOS_FALTANTES: list[int] = [97, 98, 99]

# Mapeo de SEVERIDAD (variable derivada)
SEVERIDAD_MAP: dict[int, str] = {
    0: "Leve (ambulatorio)",
    1: "Grave (hospitalizado)",
    2: "Crítico (UCI/intubado)",
    3: "Fallecido",
}

# Valor centinela para fecha de defunción (paciente vivo)
FECHA_DEF_CENTINELA: str = "9999-99-99"
