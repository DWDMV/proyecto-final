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
import matplotlib.pyplot as plt
import seaborn as sns
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
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

        preds = modelo.predict(X_test)
        
        metrics = {
            "accuracy": float(accuracy_score(y_test, preds)),
            "precision_macro": float(precision_score(y_test, preds, average="macro", zero_division=0)),
            "precision_weighted": float(precision_score(y_test, preds, average="weighted", zero_division=0)),
            "recall_macro": float(recall_score(y_test, preds, average="macro", zero_division=0)),
            "recall_weighted": float(recall_score(y_test, preds, average="weighted", zero_division=0)),
            "f1_macro": float(f1_score(y_test, preds, average="macro", zero_division=0)),
            "f1_weighted": float(f1_score(y_test, preds, average="weighted", zero_division=0)),
        }
        return metrics

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
        from sklearn.metrics import confusion_matrix

        preds = modelo.predict(X_test)
        cm = confusion_matrix(y_test, preds)
        class_names = [SEVERIDAD_MAP[i] for i in sorted(SEVERIDAD_MAP.keys())]

        plt.figure(figsize=(8, 6))
        # Formateado de colores premium
        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="YlGnBu",
            xticklabels=class_names,
            yticklabels=class_names,
            cbar=True,
            annot_kws={"size": 12, "weight": "bold"}
        )
        plt.title(f"Matriz de Confusión — {type(modelo).__name__}", fontsize=14, pad=15)
        plt.ylabel("Clase Real (True Label)", fontsize=12)
        plt.xlabel("Clase Predicha (Predicted Label)", fontsize=12)
        plt.tight_layout()
        plt.show()

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
        from sklearn.preprocessing import label_binarize
        from sklearn.metrics import roc_curve, auc

        classes = sorted(list(SEVERIDAD_MAP.keys()))
        n_classes = len(classes)
        
        # Binarizar el target para One-vs-Rest
        y_test_bin = label_binarize(y_test, classes=classes)
        y_score = modelo.predict_proba(X_test)

        fpr = dict()
        tpr = dict()
        roc_auc = dict()

        # Calcular curvas ROC por clase
        for i in range(n_classes):
            fpr[i], tpr[i], _ = roc_curve(y_test_bin[:, i], y_score[:, i])
            roc_auc[i] = auc(fpr[i], tpr[i])

        # Calcular curva ROC macro-average
        all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))
        mean_tpr = np.zeros_like(all_fpr)
        for i in range(n_classes):
            mean_tpr += np.interp(all_fpr, fpr[i], tpr[i])
        mean_tpr /= n_classes

        fpr["macro"] = all_fpr
        tpr["macro"] = mean_tpr
        roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])

        # Graficar curvas ROC
        plt.figure(figsize=(8, 6))
        
        # Macro average line
        plt.plot(
            fpr["macro"],
            tpr["macro"],
            label=f"Promedio Macro (AUC = {roc_auc['macro']:.2f})",
            color="navy",
            linestyle=":",
            linewidth=4,
        )

        colors = ["#3498db", "#2ecc71", "#e67e22", "#e74c3c"]
        for i, color in zip(range(n_classes), colors):
            label = f"{SEVERIDAD_MAP[i]} (AUC = {roc_auc[i]:.2f})"
            plt.plot(fpr[i], tpr[i], color=color, lw=2, label=label)

        plt.plot([0, 1], [0, 1], "k--", lw=1.5)
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel("Tasa de Falsos Positivos (FPR)", fontsize=12)
        plt.ylabel("Tasa de Verdaderos Positivos (TPR)", fontsize=12)
        plt.title(f"Curvas ROC One-vs-Rest — {type(modelo).__name__}", fontsize=14, pad=15)
        plt.legend(loc="lower right")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

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
        rows = []
        for nombre, modelo in modelos:
            metricas = self.evaluar(modelo, X_test, y_test)
            metricas["modelo"] = nombre
            rows.append(metricas)

        df_comp = pd.DataFrame(rows)
        # Reordenar columnas para legibilidad
        cols = ["modelo", "accuracy", "precision_macro", "recall_macro", "f1_macro", "f1_weighted"]
        df_comp = df_comp[cols]
        return df_comp

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
        from sklearn.dummy import DummyClassifier

        dummy = DummyClassifier(strategy="most_frequent")
        X_dummy_train = np.zeros((len(y_test), 1))
        dummy.fit(X_dummy_train, y_test)
        
        X_dummy_test = np.zeros((len(y_test), 1))
        
        return self.evaluar(dummy, X_dummy_test, y_test)

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
        if not hasattr(modelo, "feature_importances_"):
            print(f"El modelo {type(modelo).__name__} no cuenta con feature_importances_.")
            return

        importances = modelo.feature_importances_
        indices = np.argsort(importances)[::-1]
        
        # Crear DataFrame para graficar con seaborn
        df_imp = pd.DataFrame({
            "feature": [feature_names[i] for i in indices[:top_n]],
            "importancia": importances[indices[:top_n]]
        })

        plt.figure(figsize=(10, 6))
        sns.barplot(
            x="importancia",
            y="feature",
            data=df_imp,
            palette="viridis",
            hue="feature",
            legend=False
        )
        plt.title(f"Importancia de Variables (Top {top_n}) — {type(modelo).__name__}", fontsize=14, pad=15)
        plt.xlabel("Importancia Relativa", fontsize=12)
        plt.ylabel("Variable (Feature)", fontsize=12)
        plt.grid(True, axis="x", alpha=0.3)
        plt.tight_layout()
        plt.show()
