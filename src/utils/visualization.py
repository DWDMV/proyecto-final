"""
Funciones de visualización reutilizables para el proyecto.

Provee funciones parametrizables con estilo visual consistente para
histogramas, heatmaps, boxplots, gráficas de barras y visualizaciones
interactivas con Plotly.

Colaborador responsable: B (Análisis Exploratorio)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from typing import Optional


# ---------------------------------------------------------------------------
# Estilo global
# ---------------------------------------------------------------------------

PALETA = ["#4CAF50", "#FF9800", "#2E1AB1", "#9C27B0"]  # Leve, Grave, Crítico, Fallecido
COLOR_DEFAULT = "#5C85D6"


def configurar_estilo() -> None:
    """Configura el estilo global de matplotlib/seaborn para el proyecto.

    Aplica una paleta de colores, tamaños de fuente y estilos
    consistentes en todas las visualizaciones.
    """
    sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)
    plt.rcParams["figure.dpi"] = 120
    plt.rcParams["figure.figsize"] = (10, 5)
    plt.rcParams["axes.titleweight"] = "bold"
    plt.rcParams["axes.titlesize"] = 13


# ---------------------------------------------------------------------------
# Histograma
# ---------------------------------------------------------------------------

def histograma(
    df: pd.DataFrame,
    columna: str,
    titulo: Optional[str] = None,
    bins: int = 50,
    color: Optional[str] = None,
) -> None:
    """Genera un histograma con media, mediana y moda aproximada.

    Parameters
    ----------
    df : pd.DataFrame
    columna : str
        Nombre de la columna numérica a graficar.
    titulo : str, optional
        Título de la gráfica. Si None, se genera automáticamente.
    bins : int
        Número de bins del histograma.
    color : str, optional
        Color de las barras en formato hex. Si None usa COLOR_DEFAULT.
    """
    valores = df[columna].dropna().values
    color   = color or COLOR_DEFAULT
    titulo  = titulo or f"Distribución de {columna} — COVID-19/Influenza en México"

    media   = valores.mean()
    mediana = np.median(valores)

    counts, bin_edges = np.histogram(valores, bins=bins)
    idx_max    = np.argmax(counts)
    moda_aprox = 0.5 * (bin_edges[idx_max] + bin_edges[idx_max + 1])

    print(f"Media            = {media:.2f}")
    print(f"Mediana          = {mediana:.2f}")
    print(f"Moda (aprox)     = {moda_aprox:.2f}")

    plt.figure()
    plt.hist(valores, bins=bins, alpha=0.45, color=color, edgecolor="white")
    plt.title(titulo)
    plt.xlabel(columna)
    plt.ylabel("Frecuencia")

    plt.axvline(media,      color="tab:blue",   linestyle="--", linewidth=2,
                label=f"Media = {media:.1f}")
    plt.axvline(mediana,    color="tab:orange", linestyle="-",  linewidth=2,
                label=f"Mediana = {mediana:.1f}")
    plt.axvline(moda_aprox, color="tab:red",    linestyle=":",  linewidth=2,
                label=f"Moda (aprox) = {moda_aprox:.1f}")

    plt.legend()
    plt.tight_layout()
    plt.savefig(f"fig_histograma_{columna.lower()}.png", dpi=150, bbox_inches="tight")
    plt.show()

    # ECDF
    x_sorted = np.sort(valores)
    y = np.arange(1, x_sorted.size + 1) / x_sorted.size

    plt.figure()
    plt.step(x_sorted, y, where="post", color=color)
    plt.title(f"Función de distribución acumulada de {columna} — COVID-19/Influenza en México")
    plt.xlabel(columna)
    plt.ylabel("Proporción acumulada")
    plt.ylim(0, 1.01)
    plt.tight_layout()
    plt.show()

    p25, p50, p75, p90, p95 = np.quantile(valores, [0.25, 0.50, 0.75, 0.90, 0.95])
    print(f"P25={p25:.0f}  P50={p50:.0f}  P75={p75:.0f}  P90={p90:.0f}  P95={p95:.0f}")


# ---------------------------------------------------------------------------
# Heatmap de correlación
# ---------------------------------------------------------------------------

def heatmap_correlacion(
    df: pd.DataFrame,
    columnas: Optional[list[str]] = None,
    metodo: str = "spearman",
    titulo: str = "Correlación entre comorbilidades y severidad clínica (Spearman)",
) -> None:
    """Genera un heatmap de la matriz de correlación.

    Parameters
    ----------
    df : pd.DataFrame
    columnas : list[str], optional
        Subconjunto de columnas. Si None, usa todas las numéricas.
    metodo : str
        ``'pearson'`` o ``'spearman'``. Se recomienda Spearman para
        variables binarias u ordinales.
    titulo : str
    """
    cols = columnas if columnas else df.select_dtypes(include="number").columns.tolist()
    corr = df[cols].corr(method=metodo, numeric_only=True)

    print(f"Matriz de correlación ({metodo}):")
    print(corr.round(3).to_string())

    if "SEVERIDAD" in corr.columns:
        print(f"\nTop 10 variables más correlacionadas con SEVERIDAD:")
        top = corr["SEVERIDAD"].drop("SEVERIDAD").abs().sort_values(ascending=False).head(10)
        for var, val in top.items():
            raw = corr.loc[var, "SEVERIDAD"]
            print(f"  {var:<25} {raw:>7.3f}")

    fig, ax = plt.subplots(figsize=(13, 10))
    mask = np.triu(np.ones_like(corr, dtype=bool))

    im = ax.imshow(
        np.where(mask, np.nan, corr.values),
        cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto"
    )
    plt.colorbar(im, ax=ax, fraction=0.03, pad=0.02,
                 label=f"Correlación de {metodo.capitalize()}")

    ax.set_xticks(range(len(cols)))
    ax.set_yticks(range(len(cols)))
    ax.set_xticklabels(cols, rotation=40, ha="right", fontsize=9)
    ax.set_yticklabels(cols, fontsize=9)

    for i in range(len(corr)):
        for j in range(len(corr)):
            if not mask[i, j]:
                val = corr.iloc[i, j]
                ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                        fontsize=8, color="white" if abs(val) > 0.4 else "black")

    ax.set_title(titulo)
    plt.tight_layout()
    plt.savefig("fig_heatmap_correlacion.png", dpi=150, bbox_inches="tight")
    plt.show()


# ---------------------------------------------------------------------------
# Boxplots para outliers
# ---------------------------------------------------------------------------

def boxplots_outliers(
    df: pd.DataFrame,
    columnas: list[str],
    titulo: str = "Detección de valores atípicos en la edad de pacientes — COVID-19/Influenza",
) -> None:
    """Genera boxplots para detección de outliers con regla IQR y z-score.

    Parameters
    ----------
    df : pd.DataFrame
    columnas : list[str]
        Lista de columnas numéricas a analizar.
    titulo : str
    """
    from scipy import stats as scipy_stats

    SEVERIDAD_MAP    = {0: "Leve", 1: "Grave", 2: "Crítico", 3: "Fallecido"}
    SEVERIDAD_COLORS = ["#4CAF50", "#FF9800", "#F44336", "#9C27B0"]

    for columna in columnas:
        valores = df[columna].dropna()

        # Regla IQR
        q1  = valores.quantile(0.25)
        q3  = valores.quantile(0.75)
        iqr = q3 - q1
        lim_inf = q1 - 1.5 * iqr
        lim_sup = q3 + 1.5 * iqr
        outliers_iqr = valores[(valores < lim_inf) | (valores > lim_sup)]

        # Z-score
        z = np.abs(scipy_stats.zscore(valores))
        outliers_z = valores[z > 3]

        print(f"=== Regla IQR — {columna} ===")
        print(f"  Q1={q1:.1f}  Q3={q3:.1f}  IQR={iqr:.1f}")
        print(f"  Límite inferior : {lim_inf:.1f}")
        print(f"  Límite superior : {lim_sup:.1f}")
        print(f"  Outliers        : {len(outliers_iqr):,}  ({len(outliers_iqr)/len(valores)*100:.2f}%)")
        print(f"\n=== Z-score (|z| > 3) — {columna} ===")
        print(f"  Outliers        : {len(outliers_z):,}  ({len(outliers_z)/len(valores)*100:.2f}%)")
        if len(outliers_z) > 0:
            print(f"  Rango           : {outliers_z.min():.0f} – {outliers_z.max():.0f}")

        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        # Boxplot global
        axes[0].boxplot(valores, vert=True, patch_artist=True,
                        boxprops=dict(facecolor="#90CAF9", color="navy"),
                        medianprops=dict(color="red", linewidth=2))
        axes[0].axhline(lim_sup, color="orange", linestyle="--",
                        label=f"Límite sup. ({lim_sup:.0f})")
        axes[0].axhline(lim_inf, color="orange", linestyle=":",
                        label=f"Límite inf. ({lim_inf:.0f})")
        axes[0].set_title(f"Boxplot — {columna} (global)")
        axes[0].set_ylabel("Años")
        axes[0].legend(fontsize=8)

        # Boxplot por SEVERIDAD (si existe la columna)
        if "SEVERIDAD" in df.columns:
            df_plot = df[[columna, "SEVERIDAD"]].dropna()
            niveles = sorted(df_plot["SEVERIDAD"].unique())
            groups  = [df_plot[df_plot["SEVERIDAD"] == n][columna].values for n in niveles]
            bp = axes[1].boxplot(
                groups, patch_artist=True,
                tick_labels=[SEVERIDAD_MAP.get(int(n), n) for n in niveles]
            )
            for patch, color in zip(bp["boxes"], SEVERIDAD_COLORS):
                patch.set_facecolor(color)
                patch.set_alpha(0.7)
            axes[1].set_title(f"{columna} por nivel de SEVERIDAD")
            axes[1].set_ylabel("Años")
            axes[1].set_xlabel("Severidad")

        plt.suptitle(titulo)
        plt.tight_layout()
        plt.savefig(f"fig_boxplot_{columna.lower()}.png", dpi=150, bbox_inches="tight")
        plt.show()


# ---------------------------------------------------------------------------
# Barras categóricas
# ---------------------------------------------------------------------------

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
        Si True genera barras horizontales (útil para muchas categorías).
    """
    vc    = df[columna].value_counts().sort_index()
    total = vc.sum()
    titulo = titulo or f"Distribución de {columna}"

    colors = plt.cm.tab10(np.linspace(0, 1, len(vc)))

    fig, ax = plt.subplots(figsize=(10, 5))

    if horizontal:
        bars = ax.barh(vc.index.astype(str), vc.values, color=colors, edgecolor="white")
        for bar, n in zip(bars, vc.values):
            ax.text(n + total * 0.003,
                    bar.get_y() + bar.get_height() / 2,
                    f"{n:,} ({n/total*100:.1f}%)", va="center", fontsize=9)
        ax.set_xlabel("Frecuencia")
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    else:
        bars = ax.bar(vc.index.astype(str), vc.values, color=colors, edgecolor="white")
        for bar, n in zip(bars, vc.values):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + total * 0.005,
                    f"{n:,}\n({n/total*100:.1f}%)", ha="center", va="bottom", fontsize=9)
        ax.set_ylabel("Frecuencia")
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

    ax.set_title(titulo)
    plt.tight_layout()
    plt.savefig(f"fig_barras_{columna.lower()}.png", dpi=150, bbox_inches="tight")
    plt.show()


# ---------------------------------------------------------------------------
# Distribución del target
# ---------------------------------------------------------------------------

def distribucion_target(
    y: pd.Series,
    nombres_clases: Optional[dict] = None,
    titulo: str = "Distribución de la variable objetivo SEVERIDAD — análisis de desbalance de clases",
) -> None:
    """Visualiza la distribución del target con barras y pie chart.

    Parameters
    ----------
    y : pd.Series
        Variable objetivo (SEVERIDAD).
    nombres_clases : dict, optional
        Mapeo código → nombre. Ejemplo: {0: 'Leve', 1: 'Grave', ...}
    titulo : str
    """
    dist  = y.value_counts().sort_index()
    total = dist.sum()

    labels = [nombres_clases.get(i, str(i)) for i in dist.index] if nombres_clases \
             else dist.index.astype(str).tolist()

    colors = PALETA[:len(dist)]

    # Tabla en consola
    clase_may = dist.max()
    print(f"{'Nivel':<6} {'Descripción':<20} {'N':>8} {'%':>7} {'Ratio':>10}")
    print("-" * 58)
    for nivel, label in zip(dist.index, labels):
        n     = dist[nivel]
        ratio = clase_may / n if n > 0 else float("inf")
        print(f"  {nivel:<4} {label:<20} {n:>8,} {n/total*100:>6.1f}%  {ratio:>7.1f}:1")
    print("-" * 58)
    print(f"  {'Total':<24} {total:>8,}  100.0%")

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    # Barras
    bars = axes[0].bar(labels, dist.values, color=colors, edgecolor="white")
    for bar, n in zip(bars, dist.values):
        axes[0].text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + total * 0.002,
            f"{n:,}\n({n/total*100:.1f}%)", ha="center", va="bottom", fontsize=9
        )
    axes[0].set_title("Conteo por nivel de severidad")
    axes[0].set_ylabel("Número de pacientes")
    axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

    # Pie
    axes[1].pie(dist.values, labels=labels, colors=colors,
                autopct="%1.1f%%", startangle=140, pctdistance=0.8)
    axes[1].set_title("Proporción por nivel de severidad")

    plt.suptitle(titulo)
    plt.tight_layout()
    plt.savefig("fig_distribucion_target.png", dpi=150, bbox_inches="tight")
    plt.show()


# ---------------------------------------------------------------------------
# Scatter interactivo
# ---------------------------------------------------------------------------

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
        Columna para el eje X.
    y : str
        Columna para el eje Y.
    color : str, optional
        Columna para colorear los puntos (ej. 'SEVERIDAD').
    titulo : str
    """
    try:
        import plotly.express as px
    except ImportError:
        raise ImportError("Instala plotly: pip install plotly")

    titulo = titulo or f"{x} vs {y} — COVID-19/Influenza en México"

    fig = px.scatter(
        df,
        x=x,
        y=y,
        color=color,
        title=titulo,
        opacity=0.4,
        color_continuous_scale="RdYlGn_r" if color == "SEVERIDAD" else None,
        labels={x: x, y: y, color: color} if color else {x: x, y: y},
    )
    fig.update_traces(marker=dict(size=4))
    fig.update_layout(template="plotly_white")
    fig.show()
