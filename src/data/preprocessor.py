"""
DataPreprocessor — Pipeline de limpieza y transformación de datos.

Implementa el patrón **Pipeline**: flujo secuencial de transformaciones
(limpieza → encoding → creación de target → escalado).

Responsabilidad:
    Transformar el DataFrame crudo en un dataset limpio y listo para
    modelado, incluyendo la creación de la variable objetivo ``SEVERIDAD``.

Colaborador responsable: A (Infraestructura y Datos)
"""

import pandas as pd
import numpy as np
from typing import Optional, Tuple

from src.utils.constants import RANDOM_STATE, DATA_CLEAN_PATH


class DataPreprocessor:
    """Pipeline de preprocesamiento para el dataset COVID-19/Influenza.

    Implementa el patrón Pipeline con etapas secuenciales:
        1. Manejo de valores faltantes y códigos especiales (97, 98, 99)
        2. Creación de la variable objetivo ``SEVERIDAD``
        3. Encoding de variables categóricas
        4. Normalización / estandarización de numéricas
        5. Exportación de datos limpios

    Attributes
    ----------
    random_state : int
        Semilla para reproducibilidad.
    df_clean : pd.DataFrame | None
        DataFrame transformado tras ejecutar el pipeline.

    Examples
    --------
    >>> preprocessor = DataPreprocessor()
    >>> df_clean = preprocessor.fit_transform(df_raw)
    >>> preprocessor.exportar(df_clean)
    """

    def __init__(self, random_state: int = RANDOM_STATE):
        self.random_state = random_state
        self.df_clean: Optional[pd.DataFrame] = None

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Ejecuta el pipeline completo de transformaciones.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame crudo proveniente del DataLoader.

        Returns
        -------
        pd.DataFrame
            DataFrame limpio y listo para modelado.
        """
        # TODO: Orquestar las etapas del pipeline en orden
        raise NotImplementedError("Implementar pipeline completo")

    def _manejar_valores_faltantes(self, df: pd.DataFrame) -> pd.DataFrame:
        """Etapa 1: Manejo de nulos y códigos especiales (97, 98, 99).

        Los valores 97 ('no aplica'), 98 ('se ignora') y 99
        ('no especificado') deben tratarse como faltantes según el
        diccionario de datos de la DGE.

        Parameters
        ----------
        df : pd.DataFrame

        Returns
        -------
        pd.DataFrame
            DataFrame con valores faltantes tratados.
        """
        # TODO: Reemplazar códigos 97/98/99 y manejar NaNs
        raise NotImplementedError("Implementar manejo de valores faltantes")

    def _crear_variable_severidad(self, df: pd.DataFrame) -> pd.DataFrame:
        """Etapa 2: Creación de la variable objetivo SEVERIDAD.

        Niveles ordinales:
            0 — Leve (ambulatorio):   TIPO_PACIENTE == 1
            1 — Grave (hospitalizado): TIPO_PACIENTE == 2, sin UCI/intubación, sin defunción
            2 — Crítico (UCI/intubado): UCI == 1 OR INTUBADO == 1, sin defunción
            3 — Fallecido:            FECHA_DEF tiene valor válido (no '9999-99-99')

        Parameters
        ----------
        df : pd.DataFrame

        Returns
        -------
        pd.DataFrame
            DataFrame con columna ``SEVERIDAD`` agregada.
        """
        # TODO: Implementar lógica de derivación de SEVERIDAD
        raise NotImplementedError("Implementar creación de variable SEVERIDAD")

    def _encoding_categoricas(self, df: pd.DataFrame) -> pd.DataFrame:
        """Etapa 3: Codificación de variables categóricas.

        Parameters
        ----------
        df : pd.DataFrame

        Returns
        -------
        pd.DataFrame
            DataFrame con variables categóricas codificadas.
        """
        # TODO: Aplicar label encoding u one-hot encoding según la variable
        raise NotImplementedError("Implementar encoding de categóricas")

    def _escalar_numericas(self, df: pd.DataFrame) -> pd.DataFrame:
        """Etapa 4: Normalización o estandarización de variables numéricas.

        Parameters
        ----------
        df : pd.DataFrame

        Returns
        -------
        pd.DataFrame
            DataFrame con variables numéricas escaladas.
        """
        # TODO: Aplicar StandardScaler o MinMaxScaler
        raise NotImplementedError("Implementar escalado de numéricas")

    def exportar(self, df: pd.DataFrame, filename: str = "COVID19MEXICO_clean.csv") -> None:
        """Etapa 5: Exportar datos limpios a disco.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame limpio a guardar.
        filename : str
            Nombre del archivo de salida.
        """
        # TODO: Guardar CSV limpio en DATA_CLEAN_PATH
        raise NotImplementedError("Implementar exportación de datos limpios")

    def split_datos(
        self, df: pd.DataFrame, target_col: str = "SEVERIDAD", test_size: float = 0.2
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """Divide los datos en conjuntos de entrenamiento y prueba.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame limpio.
        target_col : str
            Nombre de la columna objetivo.
        test_size : float
            Proporción del conjunto de prueba.

        Returns
        -------
        tuple
            (X_train, X_test, y_train, y_test)
        """
        # TODO: Implementar split con stratify y random_state
        raise NotImplementedError("Implementar split de datos")
