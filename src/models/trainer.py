"""
ModelTrainer — Entrenamiento, validación cruzada y ajuste de hiperparámetros.

Responsabilidad:
    Entrenar clasificadores producidos por ``ModelFactory``, ejecutar
    validación cruzada, búsqueda de hiperparámetros y manejar el
    desbalance de clases.

Colaborador responsable: C (Modelo Supervisado)
"""

import pandas as pd
import numpy as np
from typing import Any, Optional

from src.utils.constants import RANDOM_STATE


class ModelTrainer:
    """Entrena y ajusta modelos de clasificación supervisada.

    Attributes
    ----------
    random_state : int
        Semilla para reproducibilidad en splits y búsqueda.
    best_params : dict | None
        Mejores hiperparámetros encontrados tras la búsqueda.
    cv_results : dict | None
        Resultados de validación cruzada.

    Examples
    --------
    >>> trainer = ModelTrainer()
    >>> modelo_entrenado = trainer.entrenar(modelo, X_train, y_train)
    >>> resultados_cv = trainer.validacion_cruzada(modelo, X, y, cv=5)
    """

    def __init__(self, random_state: int = RANDOM_STATE):
        self.random_state = random_state
        self.best_params: Optional[dict] = None
        self.cv_results: Optional[dict] = None

    def entrenar(self, modelo: Any, X_train: pd.DataFrame, y_train: pd.Series) -> Any:
        """Entrena un modelo con los datos de entrenamiento.

        Parameters
        ----------
        modelo : clasificador
            Instancia del modelo (de ModelFactory).
        X_train : pd.DataFrame
            Features de entrenamiento.
        y_train : pd.Series
            Variable objetivo de entrenamiento.

        Returns
        -------
        Modelo entrenado.
        """
        # TODO: Implementar entrenamiento del modelo
        raise NotImplementedError("Implementar entrenamiento")

    def validacion_cruzada(
        self, modelo: Any, X: pd.DataFrame, y: pd.Series, cv: int = 5
    ) -> dict:
        """Ejecuta validación cruzada estratificada.

        Parameters
        ----------
        modelo : clasificador
        X : pd.DataFrame
        y : pd.Series
        cv : int
            Número de folds.

        Returns
        -------
        dict
            Métricas promedio por fold.
        """
        # TODO: Implementar cross-validation con StratifiedKFold
        raise NotImplementedError("Implementar validación cruzada")

    def busqueda_hiperparametros(
        self,
        modelo: Any,
        param_grid: dict,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        cv: int = 5,
    ) -> Any:
        """Búsqueda de hiperparámetros con GridSearchCV o RandomizedSearchCV.

        Parameters
        ----------
        modelo : clasificador
        param_grid : dict
            Espacio de búsqueda de hiperparámetros.
        X_train : pd.DataFrame
        y_train : pd.Series
        cv : int

        Returns
        -------
        Mejor modelo encontrado.
        """
        # TODO: Implementar búsqueda de hiperparámetros
        raise NotImplementedError("Implementar búsqueda de hiperparámetros")

    def serializar_modelo(self, modelo: Any, nombre: str) -> None:
        """Serializa el modelo entrenado con joblib.

        Parameters
        ----------
        modelo : clasificador entrenado
        nombre : str
            Nombre del archivo (sin extensión).
        """
        # TODO: Guardar modelo en MODELS_PATH con joblib.dump
        raise NotImplementedError("Implementar serialización de modelo")
