"""
ClusterAnalyzer — Agrupamiento no supervisado de perfiles de pacientes.

Implementa K-Means y agrupamiento jerárquico (Ward) con herramientas
para selección del número de clusters, reducción de dimensionalidad
y perfilado interpretativo.

Colaborador responsable: D (Clustering)
"""

import pandas as pd
import numpy as np
from typing import Optional

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

from src.utils.constants import RANDOM_STATE


class ClusterAnalyzer:
    """Ejecuta y analiza clustering sobre el dataset de pacientes.

    Algoritmos soportados:
        - K-Means (con método del codo y coeficiente de silueta)
        - Agrupamiento jerárquico (Ward, con dendrograma)

    Attributes
    ----------
    random_state : int
    labels : np.ndarray | None
        Etiquetas de cluster asignadas tras ejecutar el algoritmo.
    n_clusters : int | None
        Número óptimo de clusters determinado.
    scaler_ : StandardScaler | None
    pca_model_ : PCA | None
    km_model_ : KMeans | None
    linkage_matrix_ : np.ndarray | None

    Examples
    --------
    >>> analyzer = ClusterAnalyzer()
    >>> analyzer.metodo_codo(X_scaled, k_range=range(2, 11))
    >>> analyzer.fit_kmeans(X_scaled, n_clusters=4)
    >>> perfiles = analyzer.perfilar_clusters(df_original, labels)
    """

    def __init__(self, random_state: int = RANDOM_STATE):
        self.random_state = random_state
        self.labels: Optional[np.ndarray] = None
        self.n_clusters: Optional[int] = None
        self.scaler_: Optional[StandardScaler] = None
        self.pca_model_: Optional[PCA] = None
        self.km_model_: Optional[KMeans] = None
        self.linkage_matrix_: Optional[np.ndarray] = None

    # ------------------------------------------------------------------
    # Preprocesamiento
    # ------------------------------------------------------------------

    def normalizar(self, df: pd.DataFrame, columnas: list[str]) -> pd.DataFrame:
        """Estandariza las columnas seleccionadas con StandardScaler.

        Parameters
        ----------
        df : pd.DataFrame
        columnas : list[str]

        Returns
        -------
        pd.DataFrame
            DataFrame con columnas estandarizadas (media=0, std=1).
        """
        X = df[columnas].copy()
        scaler = StandardScaler()
        X_arr = scaler.fit_transform(X)
        self.scaler_ = scaler
        return pd.DataFrame(X_arr, columns=columnas, index=df.index)

    # ------------------------------------------------------------------
    # Selección del número de clusters
    # ------------------------------------------------------------------

    def metodo_codo(
        self, X: pd.DataFrame, k_range: range = range(2, 11)
    ) -> dict[int, float]:
        """Grafica la inercia (WCSS) vs k y devuelve el diccionario {k: inercia}.

        Parameters
        ----------
        X : pd.DataFrame
            Datos normalizados.
        k_range : range
            Rango de valores de k a evaluar.

        Returns
        -------
        dict[int, float]
        """
        X_arr = X.values if hasattr(X, "values") else np.array(X)
        ks = list(k_range)
        inercias = []
        for k in ks:
            km = KMeans(n_clusters=k, random_state=self.random_state, n_init=10)
            km.fit(X_arr)
            inercias.append(km.inertia_)

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(ks, inercias, "bo-", linewidth=2, markersize=7)
        ax.set_xlabel("Número de clusters (k)")
        ax.set_ylabel("Inercia (WCSS)")
        ax.set_title("Método del Codo — K-Means")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
        return dict(zip(ks, inercias))

    def coeficiente_silueta(
        self, X: pd.DataFrame, k_range: range = range(2, 8)
    ) -> dict[int, float]:
        """Calcula y grafica el coeficiente de silueta promedio para cada k.

        Parameters
        ----------
        X : pd.DataFrame
        k_range : range

        Returns
        -------
        dict[int, float]
        """
        X_arr = X.values if hasattr(X, "values") else np.array(X)
        ks = list(k_range)
        scores = []
        for k in ks:
            km = KMeans(n_clusters=k, random_state=self.random_state, n_init=10)
            lbl = km.fit_predict(X_arr)
            scores.append(silhouette_score(X_arr, lbl))

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(ks, scores, "rs-", linewidth=2, markersize=7)
        ax.set_xlabel("Número de clusters (k)")
        ax.set_ylabel("Coeficiente de Silueta")
        ax.set_title("Coeficiente de Silueta vs. k")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
        return dict(zip(ks, scores))

    # ------------------------------------------------------------------
    # K-Means
    # ------------------------------------------------------------------

    def fit_kmeans(self, X: pd.DataFrame, n_clusters: int) -> np.ndarray:
        """Ajusta K-Means y almacena etiquetas y modelo.

        Parameters
        ----------
        X : pd.DataFrame
        n_clusters : int

        Returns
        -------
        np.ndarray
            Etiquetas de cluster (0-indexed).
        """
        X_arr = X.values if hasattr(X, "values") else np.array(X)
        self.n_clusters = n_clusters
        km = KMeans(n_clusters=n_clusters, random_state=self.random_state, n_init=10)
        self.labels = km.fit_predict(X_arr)
        self.km_model_ = km
        return self.labels

    # ------------------------------------------------------------------
    # Agrupamiento jerárquico
    # ------------------------------------------------------------------

    def dendrograma(
        self,
        X: pd.DataFrame,
        metodo: str = "ward",
        labels_texto: Optional[list] = None,
    ) -> np.ndarray:
        """Genera el dendrograma con scipy para una muestra de datos.

        Parameters
        ----------
        X : pd.DataFrame
            Datos (normalizados). Para legibilidad, usar ≤ 150 filas.
        metodo : str
            Método de enlace: 'ward', 'complete', 'average'.
        labels_texto : list | None
            Etiquetas de texto para cada hoja del árbol.

        Returns
        -------
        np.ndarray
            Matriz de enlaces (linkage matrix) de scipy.
        """
        from scipy.cluster.hierarchy import linkage, dendrogram

        X_arr = X.values if hasattr(X, "values") else np.array(X)
        Z = linkage(X_arr, method=metodo)

        fig_w = max(16, len(X_arr) * 0.28)
        fig, ax = plt.subplots(figsize=(fig_w, 6))
        dendrogram(
            Z,
            ax=ax,
            labels=labels_texto,
            leaf_rotation=90,
            leaf_font_size=7,
            color_threshold=0.7 * max(Z[:, 2]),
        )
        ax.set_title(
            f"COVID-19 México: Dendrograma — Agrupamiento Jerárquico ({metodo.capitalize()})"
        )
        ax.set_xlabel("Pacientes (Severidad_Índice)")
        ax.set_ylabel("Distancia euclidiana (Ward)")
        plt.tight_layout()
        plt.show()

        self.linkage_matrix_ = Z
        return Z

    def fit_jerarquico(
        self, X: pd.DataFrame, n_clusters: int, metodo: str = "ward"
    ) -> np.ndarray:
        """Ajusta AgglomerativeClustering y devuelve etiquetas.

        Parameters
        ----------
        X : pd.DataFrame
        n_clusters : int
        metodo : str

        Returns
        -------
        np.ndarray
        """
        X_arr = X.values if hasattr(X, "values") else np.array(X)
        model = AgglomerativeClustering(n_clusters=n_clusters, linkage=metodo)
        self.labels = model.fit_predict(X_arr)
        return self.labels

    # ------------------------------------------------------------------
    # Reducción de dimensionalidad y visualización
    # ------------------------------------------------------------------

    def reducir_dimensionalidad(
        self,
        X: pd.DataFrame,
        metodo: str = "pca",
        n_componentes: int = 2,
    ) -> pd.DataFrame:
        """Reduce dimensionalidad para visualización.

        Parameters
        ----------
        X : pd.DataFrame
        metodo : str
            ``'pca'`` o ``'tsne'``.
        n_componentes : int

        Returns
        -------
        pd.DataFrame
            DataFrame con columnas PC1/PC2 (o tSNE1/tSNE2).
        """
        X_arr = X.values if hasattr(X, "values") else np.array(X)
        idx = X.index if hasattr(X, "index") else None

        if metodo == "pca":
            pca = PCA(n_components=n_componentes, random_state=self.random_state)
            componentes = pca.fit_transform(X_arr)
            self.pca_model_ = pca
            cols = [f"PC{i + 1}" for i in range(n_componentes)]
            return pd.DataFrame(componentes, columns=cols, index=idx)

        if metodo == "tsne":
            from sklearn.manifold import TSNE

            tsne = TSNE(
                n_components=n_componentes,
                random_state=self.random_state,
                perplexity=30,
            )
            componentes = tsne.fit_transform(X_arr)
            cols = [f"tSNE{i + 1}" for i in range(n_componentes)]
            return pd.DataFrame(componentes, columns=cols, index=idx)

        raise ValueError(f"Método '{metodo}' no soportado. Usar 'pca' o 'tsne'.")

    def visualizar_clusters(
        self,
        X_reducido: pd.DataFrame,
        labels: np.ndarray,
        titulo: str = "Clusters",
    ) -> None:
        """Scatter plot coloreado por cluster.

        Parameters
        ----------
        X_reducido : pd.DataFrame
            DataFrame con exactamente 2 columnas (componentes 2D).
        labels : np.ndarray
            Etiquetas de cluster alineadas posicionalmente con X_reducido.
        titulo : str
        """
        n_cl = len(np.unique(labels))
        cmap = plt.colormaps["tab10"].resampled(n_cl)

        fig, ax = plt.subplots(figsize=(8, 6))
        X_arr = X_reducido.values
        col0, col1 = X_reducido.columns[0], X_reducido.columns[1]

        for cl in sorted(np.unique(labels)):
            mask = labels == cl
            ax.scatter(
                X_arr[mask, 0],
                X_arr[mask, 1],
                c=[cmap(cl)],
                label=f"Cluster {cl}",
                alpha=0.6,
                s=20,
            )

        ax.set_xlabel(col0)
        ax.set_ylabel(col1)
        ax.set_title(titulo)
        ax.legend(markerscale=2)
        plt.tight_layout()
        plt.show()

    # ------------------------------------------------------------------
    # Perfilado
    # ------------------------------------------------------------------

    def perfilar_clusters(
        self,
        df: pd.DataFrame,
        labels: np.ndarray,
    ) -> pd.DataFrame:
        """Estadísticas descriptivas por cluster para interpretación.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame original (no escalado) para interpretabilidad.
        labels : np.ndarray
            Etiquetas de cluster alineadas con df.

        Returns
        -------
        pd.DataFrame
            Tabla con media de cada variable numérica por cluster,
            más la columna n_pacientes.
        """
        df_c = df.copy().reset_index(drop=True)
        df_c["Cluster"] = labels
        cols_num = df_c.select_dtypes(include=[np.number]).columns.tolist()
        cols_num = [c for c in cols_num if c != "Cluster"]
        perfiles = df_c.groupby("Cluster")[cols_num].mean().round(3)
        perfiles.insert(0, "n_pacientes", df_c.groupby("Cluster").size())
        return perfiles
