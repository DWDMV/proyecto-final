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

from src.utils.constants import (
    RANDOM_STATE,
    DATA_CLEAN_PATH,
    COLS_COMORBILIDADES,
    FECHA_DEF_CENTINELA,
)


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
        self._edad_scaler = None

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
        df = self._manejar_valores_faltantes(df)
        df = self._crear_variable_severidad(df)
        df = self._encoding_categoricas(df)
        df = self._escalar_numericas(df)
        self.df_clean = df
        return df

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
        df = df.copy()

        # Comorbilidades: 98 = "se ignora"
        for col in COLS_COMORBILIDADES:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
                df[col] = df[col].replace({97: np.nan, 98: np.nan, 99: np.nan})

        # Variables clínicas usadas para derivar SEVERIDAD
        for col in ["INTUBADO", "UCI", "NEUMONIA", "TIPO_PACIENTE"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
                df[col] = df[col].replace({97: np.nan, 98: np.nan, 99: np.nan})

        # Variables demográficas binarias
        for col in ["SEXO", "EMBARAZO", "HABLA_LENGUA_INDIG", "INDIGENA",
                    "MIGRANTE", "OTRO_CASO", "NACIONALIDAD"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
                df[col] = df[col].replace({97: np.nan, 98: np.nan, 99: np.nan})

        # EDAD como numérico
        df["EDAD"] = pd.to_numeric(df["EDAD"], errors="coerce")

        # Fechas de eventos
        for col in ["FECHA_INGRESO", "FECHA_SINTOMAS", "FECHA_ACTUALIZACION"]:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")

        # FECHA_DEF: la centinela '9999-99-99' significa paciente vivo → NaT
        if "FECHA_DEF" in df.columns:
            df["FECHA_DEF"] = df["FECHA_DEF"].replace(FECHA_DEF_CENTINELA, pd.NaT)
            df["FECHA_DEF"] = pd.to_datetime(df["FECHA_DEF"], errors="coerce")

        return df

    def _crear_variable_severidad(self, df: pd.DataFrame) -> pd.DataFrame:
        """Etapa 2: Creación de la variable objetivo SEVERIDAD.

        Niveles ordinales (prioridad descendente):
            3 — Fallecido:             FECHA_DEF tiene fecha válida
            2 — Crítico (UCI/intubado): UCI == 1 OR INTUBADO == 1
            1 — Grave (hospitalizado): TIPO_PACIENTE == 2
            0 — Leve (ambulatorio):    TIPO_PACIENTE == 1

        Parameters
        ----------
        df : pd.DataFrame

        Returns
        -------
        pd.DataFrame
            DataFrame con columna ``SEVERIDAD`` agregada.
        """
        df = df.copy()

        sev = np.zeros(len(df), dtype=int)

        sev = np.where(df["TIPO_PACIENTE"] == 2, 1, sev)
        sev = np.where((df["UCI"] == 1) | (df["INTUBADO"] == 1), 2, sev)
        sev = np.where(df["FECHA_DEF"].notna(), 3, sev)

        df["SEVERIDAD"] = sev
        return df

    def _encoding_categoricas(self, df: pd.DataFrame) -> pd.DataFrame:
        """Etapa 3: Codificación de variables categóricas.

        Convierte columnas binarias (1=Sí / 2=No) a (1 / 0).
        SEXO: 1=Mujer → 0, 2=Hombre → 1.

        Parameters
        ----------
        df : pd.DataFrame

        Returns
        -------
        pd.DataFrame
            DataFrame con variables categóricas codificadas.
        """
        df = df.copy()

        # Comorbilidades + variables clínicas: 1=Sí→1, 2=No→0
        binary_si_no = COLS_COMORBILIDADES + [
            "NEUMONIA", "TOMA_MUESTRA_LAB", "INTUBADO", "UCI",
            "EMBARAZO", "HABLA_LENGUA_INDIG", "INDIGENA", "MIGRANTE",
            "OTRO_CASO", "NACIONALIDAD",
        ]
        for col in binary_si_no:
            if col in df.columns:
                df[col] = df[col].map({1: 1, 2: 0})

        # TIPO_PACIENTE: 1=ambulatorio→0, 2=hospitalizado→1
        if "TIPO_PACIENTE" in df.columns:
            df["TIPO_PACIENTE"] = df["TIPO_PACIENTE"].map({1: 0, 2: 1})

        # SEXO: 1=Mujer→0, 2=Hombre→1
        if "SEXO" in df.columns:
            df["SEXO"] = df["SEXO"].map({1: 0, 2: 1})

        return df

    def _escalar_numericas(self, df: pd.DataFrame) -> pd.DataFrame:
        """Etapa 4: Estandarización de variables numéricas continuas.

        Agrega ``EDAD_SCALED`` (StandardScaler sobre EDAD) manteniendo
        la columna original para interpretabilidad en EDA.

        Parameters
        ----------
        df : pd.DataFrame

        Returns
        -------
        pd.DataFrame
            DataFrame con ``EDAD_SCALED`` agregada.
        """
        from sklearn.preprocessing import StandardScaler

        df = df.copy()

        if "EDAD" in df.columns:
            scaler = StandardScaler()
            mask = df["EDAD"].notna()
            df.loc[mask, "EDAD_SCALED"] = scaler.fit_transform(
                df.loc[mask, ["EDAD"]]
            ).flatten()
            self._edad_scaler = scaler

        return df

    def exportar(self, df: pd.DataFrame, filename: str = "COVID19MEXICO_clean.csv") -> None:
        """Etapa 5: Exportar datos limpios a disco.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame limpio a guardar.
        filename : str
            Nombre del archivo de salida.
        """
        output_path = DATA_CLEAN_PATH / filename
        df.to_csv(output_path, index=False, encoding="utf-8")
        print(f"Dataset limpio exportado a: {output_path}")
        print(f"Dimensiones: {df.shape[0]:,} filas × {df.shape[1]} columnas")

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
        from sklearn.model_selection import train_test_split

        cols_no_feature = [
            target_col, "ID_REGISTRO", "FECHA_ACTUALIZACION",
            "FECHA_INGRESO", "FECHA_SINTOMAS", "FECHA_DEF",
            "PAIS_NACIONALIDAD", "PAIS_ORIGEN",
        ]
        drop_cols = [c for c in cols_no_feature if c in df.columns]

        X = df.drop(columns=drop_cols)
        y = df[target_col]

        return train_test_split(
            X, y,
            test_size=test_size,
            random_state=self.random_state,
            stratify=y,
        )
