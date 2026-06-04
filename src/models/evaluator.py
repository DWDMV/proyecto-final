"""
ModelEvaluator — Métricas de evaluación y visualizaciones de rendimiento.

Responsabilidad:
    Calcular todas las métricas requeridas (accuracy, precision, recall,
    F1, ROC/AUC) y generar visualizaciones de evaluación (matriz de
    confusión, curvas ROC, comparativas entre modelos).

Colaborador responsable: C (Modelo Supervisado)
"""

import pandas as pd
import numpy as np
from typing import Any, Optional

from src.utils.constants import SEVERIDAD_MAP


class ModelEvaluator:
    """Evalúa modelos de clasificación con métricas completas.

    Genera:
        - Accuracy, Precision, Recall, F1-score (macro y ponderado)
        - Matriz de confusión (visualización)
        - Curva ROC y AUC (One-vs-Rest para multi-clase)
        - Comparación con baseline (clasificador mayoritario)
        - Feature importance ranking

    Examples
    --------
    >>> evaluator = ModelEvaluator()
    >>> metricas = evaluator.evaluar(modelo, X_test, y_test)
    >>> evaluator.matriz_confusion(modelo, X_test, y_test)
    >>> evaluator.comparar_modelos([modelo_dt, modelo_rf, modelo_xgb], X_test, y_test)
    """

    def __init__(self):
        self.resultados: dict = {}

    def evaluar(self, modelo: Any, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
        """Calcula todas las métricas de evaluación.

        Parameters
        ----------
        modelo : clasificador entrenado
        X_test : pd.DataFrame
        y_test : pd.Series

        Returns
        -------
        dict
            Diccionario con accuracy, precision, recall, f1_macro,
            f1_weighted.
        """
        # TODO: Implementar cálculo de métricas completas
        raise NotImplementedError("Implementar evaluación de modelo")

    def matriz_confusion(
        self, modelo: Any, X_test: pd.DataFrame, y_test: pd.Series
    ) -> None:
        """Genera y visualiza la matriz de confusión.

        Parameters
        ----------
        modelo : clasificador entrenado
        X_test : pd.DataFrame
        y_test : pd.Series
        """
        # TODO: Implementar visualización de matriz de confusión
        raise NotImplementedError("Implementar matriz de confusión")

    def curva_roc(
        self, modelo: Any, X_test: pd.DataFrame, y_test: pd.Series
    ) -> None:
        """Genera curvas ROC y calcula AUC (One-vs-Rest para multi-clase).

        Parameters
        ----------
        modelo : clasificador entrenado
        X_test : pd.DataFrame
        y_test : pd.Series
        """
        # TODO: Implementar curvas ROC multi-clase
        raise NotImplementedError("Implementar curva ROC")

    def comparar_modelos(
        self,
        modelos: list[tuple[str, Any]],
        X_test: pd.DataFrame,
        y_test: pd.Series,
    ) -> pd.DataFrame:
        """Compara métricas de múltiples modelos en una tabla.

        Parameters
        ----------
        modelos : list[tuple[str, Any]]
            Lista de tuplas (nombre, modelo_entrenado).
        X_test : pd.DataFrame
        y_test : pd.Series

        Returns
        -------
        pd.DataFrame
            Tabla comparativa de métricas.
        """
        # TODO: Implementar comparación entre DT, RF y XGBoost
        raise NotImplementedError("Implementar comparación de modelos")

    def evaluar_baseline(self, y_test: pd.Series) -> dict:
        """Evalúa un clasificador mayoritario como línea base.

        Parameters
        ----------
        y_test : pd.Series

        Returns
        -------
        dict
            Métricas del baseline.
        """
        # TODO: Implementar baseline (clasificador mayoritario)
        raise NotImplementedError("Implementar evaluación de baseline")

    def feature_importance(
        self, modelo: Any, feature_names: list[str], top_n: int = 15
    ) -> None:
        """Visualiza las features más importantes del modelo.

        Parameters
        ----------
        modelo : clasificador entrenado (con ``feature_importances_``)
        feature_names : list[str]
        top_n : int
        """
        # TODO: Implementar visualización de feature importances
        raise NotImplementedError("Implementar feature importance")
