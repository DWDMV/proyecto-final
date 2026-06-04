"""
Funciones de visualización reutilizables para el proyecto.

Provee funciones parametrizables con estilo visual consistente para
histogramas, heatmaps, boxplots, gráficas de barras y visualizaciones
interactivas con Plotly.

Colaborador responsable: B (Análisis Exploratorio)
"""

import pandas as pd
import numpy as np
from typing import Optional


# ---------------------------------------------------------------------------
# Estilo global
# ---------------------------------------------------------------------------

# TODO: Definir paleta de colores y estilo consistente para el proyecto
# Ejemplo: PALETA = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3B1F2B']


def configurar_estilo() -> None:
    """Configura el estilo global de matplotlib/seaborn para el proyecto.

    Aplica una paleta de colores, tamaños de fuente y estilos
    consistentes en todas las visualizaciones.
    """
    # TODO: Implementar configuración de estilo global
    raise NotImplementedError("Implementar configuración de estilo")


def histograma(
    df: pd.DataFrame,
    columna: str,
    titulo: Optional[str] = None,
    bins: int = 30,
    color: Optional[str] = None,
) -> None:
    """Genera un histograma con interpretación visual.

    Parameters
    ----------
    df : pd.DataFrame
    columna : str
    titulo : str, optional
    bins : int
    color : str, optional
    """
    # TODO: Implementar histograma con matplotlib/seaborn
    raise NotImplementedError("Implementar histograma")


def heatmap_correlacion(
    df: pd.DataFrame,
    columnas: Optional[list[str]] = None,
    metodo: str = "pearson",
    titulo: str = "Matriz de Correlación",
) -> None:
    """Genera un heatmap de la matriz de correlación.

    Parameters
    ----------
    df : pd.DataFrame
    columnas : list[str], optional
        Subconjunto de columnas. Si None, usa todas las numéricas.
    metodo : str
        ``'pearson'`` o ``'spearman'``.
    titulo : str
    """
    # TODO: Implementar heatmap de correlación
    raise NotImplementedError("Implementar heatmap de correlación")


def boxplots_outliers(
    df: pd.DataFrame,
    columnas: list[str],
    titulo: str = "Detección de Valores Atípicos",
) -> None:
    """Genera boxplots para detección de outliers.

    Parameters
    ----------
    df : pd.DataFrame
    columnas : list[str]
    titulo : str
    """
    # TODO: Implementar boxplots con regla IQR
    raise NotImplementedError("Implementar boxplots para outliers")


def barras_categoricas(
    df: pd.DataFrame,
    columna: str,
    titulo: Optional[str] = None,
    horizontal: bool = False,
) -> None:
    """Genera gráfica de barras con frecuencias para variables categóricas.

    Parameters
    ----------
    df : pd.DataFrame
    columna : str
    titulo : str, optional
    horizontal : bool
    """
    # TODO: Implementar gráfica de barras
    raise NotImplementedError("Implementar gráfica de barras categóricas")


def distribucion_target(
    y: pd.Series,
    nombres_clases: Optional[dict] = None,
    titulo: str = "Distribución de la Variable Objetivo",
) -> None:
    """Visualiza la distribución del target (balance de clases).

    Parameters
    ----------
    y : pd.Series
        Variable objetivo.
    nombres_clases : dict, optional
        Mapeo de código → nombre legible.
    titulo : str
    """
    # TODO: Implementar visualización de balance de clases
    raise NotImplementedError("Implementar distribución del target")


def scatter_interactivo(
    df: pd.DataFrame,
    x: str,
    y: str,
    color: Optional[str] = None,
    titulo: str = "",
) -> None:
    """Genera un scatter plot interactivo con Plotly.

    Parameters
    ----------
    df : pd.DataFrame
    x : str
    y : str
    color : str, optional
        Columna para colorear puntos.
    titulo : str
    """
    # TODO: Implementar scatter plot interactivo con Plotly
    raise NotImplementedError("Implementar scatter interactivo")
