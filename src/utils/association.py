"""
AssociationRuleMiner — Reglas de asociación para comorbilidades.

Aplica Apriori sobre las variables binarias de comorbilidades para
descubrir combinaciones frecuentes no intuitivas en la población mexicana.

Colaborador responsable: B (Análisis Exploratorio)
"""

import pandas as pd
from typing import Optional

from mlxtend.frequent_patterns import apriori, association_rules
from src.utils.constants import COLS_COMORBILIDADES


class AssociationRuleMiner:
    """Descubre reglas de asociación entre comorbilidades.

    Utiliza la librería ``mlxtend`` para ejecutar Apriori y extraer
    reglas con métricas de soporte, confianza y lift.

    Attributes
    ----------
    reglas : pd.DataFrame | None
        DataFrame con las reglas descubiertas y sus métricas.
    itemsets_frecuentes : pd.DataFrame | None
        Itemsets frecuentes encontrados.

    Examples
    --------
    >>> miner = AssociationRuleMiner()
    >>> df_binario = miner.preparar_datos(df)
    >>> miner.ejecutar_apriori(df_binario, min_support=0.05)
    >>> miner.generar_reglas(metric="lift", min_threshold=1.0)
    >>> miner.top_reglas(n=20)
    """

    def __init__(self):
        self.reglas: Optional[pd.DataFrame] = None
        self.itemsets_frecuentes: Optional[pd.DataFrame] = None

    def preparar_datos(
        self, df: pd.DataFrame, columnas: list[str] = COLS_COMORBILIDADES
    ) -> pd.DataFrame:
        """Prepara las variables binarias para reglas de asociación.

        El CSV limpio ya tiene las comorbilidades en 0/1 (encoding
        aplicado en el preprocesamiento). Este método solo selecciona
        las columnas relevantes, descarta filas con NaN y convierte
        a booleano, que es el formato que requiere mlxtend.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame limpio exportado por el notebook 01.
        columnas : list[str]
            Lista de columnas binarias a incluir.
            Por defecto usa COLS_COMORBILIDADES.

        Returns
        -------
        pd.DataFrame
            DataFrame booleano (True/False) sin NaN, listo para Apriori.
        """
        # Seleccionar solo las columnas disponibles
        cols_presentes = [c for c in columnas if c in df.columns]

        # Descartar filas donde todas las comorbilidades sean NaN
        df_sel = df[cols_presentes].dropna(how="all")

        # Filas con algún NaN se rellenan con 0 (ausencia de información = no reportado)
        df_sel = df_sel.fillna(0)

        # Convertir a booleano — mlxtend requiere este formato
        df_bool = df_sel.astype(bool)

        print(f"Registros usados para Apriori : {len(df_bool):,}")
        print(f"Comorbilidades analizadas     : {list(df_bool.columns)}")

        return df_bool

    def ejecutar_apriori(
        self, df_binario: pd.DataFrame, min_support: float = 0.05
    ) -> pd.DataFrame:
        """Ejecuta el algoritmo Apriori para encontrar itemsets frecuentes.

        Parameters
        ----------
        df_binario : pd.DataFrame
            DataFrame booleano devuelto por ``preparar_datos``.
        min_support : float
            Soporte mínimo (proporción de registros) para considerar
            un itemset como frecuente. Por defecto 0.05 (5 %).

        Returns
        -------
        pd.DataFrame
            Itemsets frecuentes con su soporte.

        Raises
        ------
        ValueError
            Si ``df_binario`` está vacío o no contiene columnas booleanas.
        """
        if df_binario.empty:
            raise ValueError("df_binario está vacío. Revisa preparar_datos().")

        self.itemsets_frecuentes = apriori(
            df_binario,
            min_support=min_support,
            use_colnames=True,
            verbose=0
        )

        print(f"Itemsets frecuentes encontrados (soporte ≥ {min_support}): "
              f"{len(self.itemsets_frecuentes)}")

        return self.itemsets_frecuentes

    def generar_reglas(
        self,
        metric: str = "lift",
        min_threshold: float = 1.0,
    ) -> pd.DataFrame:
        """Genera reglas de asociación a partir de los itemsets frecuentes.

        Debe llamarse después de ``ejecutar_apriori``.

        Parameters
        ----------
        metric : str
            Métrica para filtrar reglas: ``'lift'``, ``'confidence'``
            o ``'support'``.
        min_threshold : float
            Valor mínimo de la métrica para incluir una regla.
            Para lift se recomienda ≥ 1.0 (asociación positiva).

        Returns
        -------
        pd.DataFrame
            Reglas con columnas: antecedents, consequents, support,
            confidence, lift.

        Raises
        ------
        RuntimeError
            Si se llama antes de ``ejecutar_apriori``.
        """
        if self.itemsets_frecuentes is None:
            raise RuntimeError("Primero ejecuta ejecutar_apriori().")

        self.reglas = association_rules(
            self.itemsets_frecuentes,
            metric=metric,
            min_threshold=min_threshold
        )

        # Ordenar por lift descendente por defecto
        self.reglas = self.reglas.sort_values("lift", ascending=False).reset_index(drop=True)

        print(f"Reglas generadas (metric='{metric}' ≥ {min_threshold}): "
              f"{len(self.reglas)}")

        return self.reglas

    def top_reglas(self, n: int = 20, ordenar_por: str = "lift") -> pd.DataFrame:
        """Retorna las top-N reglas ordenadas por la métrica indicada.

        Formatea antecedentes y consecuentes como strings legibles
        para facilitar la interpretación clínica.

        Parameters
        ----------
        n : int
            Número de reglas a retornar.
        ordenar_por : str
            Columna por la que ordenar: ``'lift'``, ``'confidence'``
            o ``'support'``.

        Returns
        -------
        pd.DataFrame
            Top-N reglas con columnas legibles.

        Raises
        ------
        RuntimeError
            Si se llama antes de ``generar_reglas``.
        """
        if self.reglas is None:
            raise RuntimeError("Primero ejecuta generar_reglas().")

        top = (
            self.reglas
            .sort_values(ordenar_por, ascending=False)
            .head(n)
            .copy()
        )

        top["antecedents"] = top["antecedents"].apply(lambda x: ", ".join(sorted(x)))
        top["consequents"] = top["consequents"].apply(lambda x: ", ".join(sorted(x)))

        # Seleccionar y renombrar columnas relevantes
        top = top[["antecedents", "consequents", "support", "confidence", "lift"]].round(4)
        top.columns = ["Antecedente", "Consecuente", "Soporte", "Confianza", "Lift"]

        return top.reset_index(drop=True)
