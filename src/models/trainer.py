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
import joblib

from src.utils.constants import RANDOM_STATE, MODELS_PATH


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
        # Si es XGBClassifier, calculamos e inyectamos los pesos de clase mediante sample_weight
        if type(modelo).__name__ == "XGBClassifier":
            from sklearn.utils.class_weight import compute_sample_weight
            sample_weight = compute_sample_weight(class_weight="balanced", y=y_train)
            modelo.fit(X_train, y_train, sample_weight=sample_weight)
        else:
            modelo.fit(X_train, y_train)
        return modelo

    def validacion_cruzada(
        self, modelo: Any, X: pd.DataFrame, y: pd.Series, cv: int = 5
    ) -> dict:
        """Ejecuta validación cruzada estratificada con soporte para pesos de clase.

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
        from sklearn.model_selection import StratifiedKFold
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        from sklearn.utils.class_weight import compute_sample_weight
        from sklearn.base import clone

        skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=self.random_state)
        
        metrics = {
            "accuracy": [],
            "precision_macro": [],
            "recall_macro": [],
            "f1_macro": [],
            "f1_weighted": []
        }

        for train_idx, val_idx in skf.split(X, y):
            X_train_fold = X.iloc[train_idx]
            y_train_fold = y.iloc[train_idx]
            X_val_fold = X.iloc[val_idx]
            y_val_fold = y.iloc[val_idx]

            # Clonar el modelo para garantizar un entrenamiento limpio por fold
            model_fold = clone(modelo)

            if type(model_fold).__name__ == "XGBClassifier":
                sw = compute_sample_weight(class_weight="balanced", y=y_train_fold)
                model_fold.fit(X_train_fold, y_train_fold, sample_weight=sw)
            else:
                model_fold.fit(X_train_fold, y_train_fold)

            preds = model_fold.predict(X_val_fold)
            
            metrics["accuracy"].append(accuracy_score(y_val_fold, preds))
            metrics["precision_macro"].append(precision_score(y_val_fold, preds, average="macro", zero_division=0))
            metrics["recall_macro"].append(recall_score(y_val_fold, preds, average="macro", zero_division=0))
            metrics["f1_macro"].append(f1_score(y_val_fold, preds, average="macro", zero_division=0))
            metrics["f1_weighted"].append(f1_score(y_val_fold, preds, average="weighted", zero_division=0))

        # Promediar métricas
        cv_results = {k: float(np.mean(v)) for k, v in metrics.items()}
        self.cv_results = cv_results
        return cv_results

    def busqueda_hiperparametros(
        self,
        modelo: Any,
        param_grid: dict,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        cv: int = 5,
    ) -> Any:
        """Búsqueda de hiperparámetros con RandomizedSearchCV optimizando f1_macro.

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
        from sklearn.model_selection import RandomizedSearchCV

        fit_params = {}
        if type(modelo).__name__ == "XGBClassifier":
            from sklearn.utils.class_weight import compute_sample_weight
            sw = compute_sample_weight(class_weight="balanced", y=y_train)
            fit_params["sample_weight"] = sw

        search = RandomizedSearchCV(
            estimator=modelo,
            param_distributions=param_grid,
            n_iter=10,
            scoring="f1_macro",
            cv=cv,
            random_state=self.random_state,
            n_jobs=-1,
        )
        search.fit(X_train, y_train, **fit_params)
        
        self.best_params = search.best_params_
        return search.best_estimator_

    def serializar_modelo(self, modelo: Any, nombre: str) -> None:
        """Serializa el modelo entrenado con joblib.

        Parameters
        ----------
        modelo : clasificador entrenado
        nombre : str
            Nombre del archivo (sin extensión).
        """
        MODELS_PATH.mkdir(parents=True, exist_ok=True)
        filepath = MODELS_PATH / f"{nombre}.joblib"
        joblib.dump(modelo, filepath)
        print(f"Modelo guardado en: {filepath}")
