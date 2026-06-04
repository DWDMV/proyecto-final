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
        # TODO: Implementar carga del CSV con tipos de datos optimizados
        raise NotImplementedError("Implementar carga del CSV")

    def resumen_calidad(self) -> pd.DataFrame:
        """Genera un resumen de calidad de datos por columna.

        Incluye: tipo de dato, conteo de nulos, porcentaje de nulos,
        valores únicos.

        Returns
        -------
        pd.DataFrame
            Tabla resumen de calidad.
        """
        # TODO: Implementar resumen de calidad
        raise NotImplementedError("Implementar resumen de calidad")

    def detectar_duplicados(self) -> int:
        """Identifica y cuenta registros duplicados.

        Returns
        -------
        int
            Número de filas duplicadas encontradas.
        """
        # TODO: Implementar detección de duplicados
        raise NotImplementedError("Implementar detección de duplicados")

    def descripcion_general(self) -> dict:
        """Retorna un diccionario con metadatos generales del dataset.

        Returns
        -------
        dict
            Claves: 'filas', 'columnas', 'tipos', 'memoria_mb'.
        """
        # TODO: Implementar descripción general
        raise NotImplementedError("Implementar descripción general")
