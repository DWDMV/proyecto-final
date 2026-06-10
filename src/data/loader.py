"""
DataLoader — Carga y validación del dataset COVID-19/Influenza de la DGE.

Responsabilidad:
    Leer el archivo CSV crudo, validar su estructura (dimensiones, tipos),
    reportar estadísticas de calidad (nulos, duplicados) y proveer acceso
    limpio al DataFrame.

Colaborador responsable: A (Infraestructura y Datos)
"""

import pandas as pd
from pathlib import Path
from typing import Optional

from src.utils.constants import DATA_RAW_PATH, CSV_FILENAME


class DataLoader:
    """Carga y valida el dataset de la DGE desde un archivo CSV.

    Attributes
    ----------
    filepath : Path
        Ruta absoluta al archivo CSV.
    df : pd.DataFrame | None
        DataFrame cargado; ``None`` hasta que se invoque ``load()``.

    Examples
    --------
    >>> loader = DataLoader()
    >>> df = loader.load()
    >>> loader.resumen_calidad()
    """

    def __init__(self, filepath: Optional[Path] = None):
        """Inicializa el DataLoader.

        Parameters
        ----------
        filepath : Path, optional
            Ruta al CSV. Si no se proporciona, usa la ruta por defecto
            definida en ``constants.py``.
        """
        self.filepath = filepath or DATA_RAW_PATH / CSV_FILENAME
        self.df: Optional[pd.DataFrame] = None

    def load(self) -> pd.DataFrame:
        """Carga el CSV en un DataFrame de pandas.

        Returns
        -------
        pd.DataFrame
            El dataset completo sin transformaciones.

        Raises
        ------
        FileNotFoundError
            Si el archivo CSV no existe en la ruta especificada.
        """
        if not self.filepath.exists():
            raise FileNotFoundError(f"No se encontró el archivo: {self.filepath}")
        self.df = pd.read_csv(self.filepath, encoding="utf-8", low_memory=False)
        self.df.columns = self.df.columns.str.strip()
        return self.df

    def resumen_calidad(self) -> pd.DataFrame:
        """Genera un resumen de calidad de datos por columna.

        Incluye: tipo de dato, conteo de nulos, porcentaje de nulos,
        valores únicos y conteo de códigos especiales (97, 98, 99).

        Returns
        -------
        pd.DataFrame
            Tabla resumen de calidad.
        """
        if self.df is None:
            raise RuntimeError("Ejecuta load() antes de llamar a resumen_calidad()")
        rows = []
        for col in self.df.columns:
            nulos = int(self.df[col].isna().sum())
            especiales = int(
                self.df[col].astype(str).str.strip().isin(["97", "98", "99"]).sum()
            )
            rows.append(
                {
                    "columna": col,
                    "tipo": str(self.df[col].dtype),
                    "nulos": nulos,
                    "pct_nulos": f"{nulos / len(self.df) * 100:.2f}",
                    "codigos_especiales": especiales,
                    "pct_especiales": f"{especiales / len(self.df) * 100:.2f}",
                    "valores_unicos": self.df[col].nunique(),
                }
            )
        return pd.DataFrame(rows)

    def detectar_duplicados(self) -> int:
        """Identifica y cuenta registros duplicados.

        Returns
        -------
        int
            Número de filas duplicadas encontradas.
        """
        if self.df is None:
            raise RuntimeError("Ejecuta load() antes de llamar a detectar_duplicados()")
        n = int(self.df.duplicated().sum())
        print(f"Registros duplicados: {n} ({n / len(self.df) * 100:.2f}%)")
        return n

    def descripcion_general(self) -> dict:
        """Retorna un diccionario con metadatos generales del dataset.

        Returns
        -------
        dict
            Claves: 'filas', 'columnas', 'tipos', 'memoria_mb'.
        """
        if self.df is None:
            raise RuntimeError("Ejecuta load() antes de llamar a descripcion_general()")
        info = {
            "filas": self.df.shape[0],
            "columnas": self.df.shape[1],
            "tipos": {str(k): int(v) for k, v in self.df.dtypes.value_counts().items()},
            "memoria_mb": round(self.df.memory_usage(deep=True).sum() / 1024**2, 2),
        }
        print(f"Filas     : {info['filas']:,}")
        print(f"Columnas  : {info['columnas']}")
        print(f"Memoria   : {info['memoria_mb']} MB")
        for dtype, count in info["tipos"].items():
            print(f"  {dtype}: {count} col(s)")
        return info
