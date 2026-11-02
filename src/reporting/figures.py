"""Figuras del análisis exploratorio (sección 22).

Cada figura lleva título con unidad, período, departamento cuando corresponde,
fuente y si los valores son observados, agregados o predichos.

Colores: paleta categórica de referencia en orden fijo por departamento
(validada para daltonismo en pares adyacentes); rampa ordinal azul para las
categorías del CI; rampa divergente azul–gris–rojo para correlaciones y z.
"""

import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

from src.features.chill_index import CATEGORY_LABELS  # noqa: E402

SURFACE = "#fcfcfb"
TEXT = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"

# Orden fijo: el color sigue al departamento en todas las figuras.
DEPARTMENT_COLORS = {2: "#2a78d6", 4: "#eb6834", 15: "#1baf7a", 18: "#eda100", 19: "#e87ba4"}
WINDOW_COLORS = {"ejercicio": "#2a78d6", "jul_oct": "#eb6834"}
ORDINAL_BLUE = ["#86b6ef", "#3987e5", "#1c5cab", "#0d366b"]
SEQUENTIAL_BLUE = LinearSegmentedColormap.from_list(
    "seq_blue", ["#f0efec", "#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"]
)
DIVERGING = LinearSegmentedColormap.from_list(
    "div_blue_red", ["#1c5cab", "#86b6ef", "#f0efec", "#f2a09f", "#c23a39"]
)

SOURCE_SNIG = "SNIG/DICOSE"
SOURCE_INIA = "INIA (banco agroclimático)"

plt.rcParams.update(
    {
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "axes.edgecolor": AXIS,
        "axes.labelcolor": TEXT_SECONDARY,
        "axes.titlecolor": TEXT,
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "axes.grid": True,
        "axes.axisbelow": True,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "grid.color": GRID,
        "grid.linewidth": 0.6,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "xtick.labelcolor": TEXT_SECONDARY,
        "ytick.labelcolor": TEXT_SECONDARY,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.frameon": False,
        "legend.fontsize": 8,
        "legend.labelcolor": TEXT_SECONDARY,
        "font.size": 9,
        "lines.linewidth": 2,
    }
)


def _finish(fig, title: str, subtitle: str, caption: str, path: Path, legend_from=None) -> Path:
    """Título, subtítulo, leyenda (en su propia franja, sin tapar marcas) y pie con fuente.

    Las posiciones se fijan en pulgadas para que no dependan de la altura de la figura.
    """
    width, height = fig.get_size_inches()
    top = 1 - 0.25 / height
    fig.text(0.01, top, title, ha="left", va="top", fontsize=12, color=TEXT, fontweight="bold")
    fig.text(0.01, top - 0.27 / height, subtitle, ha="left", va="top", fontsize=9, color=TEXT_SECONDARY)
    header = 0.75
    if legend_from is not None:
        handles, labels = legend_from.get_legend_handles_labels()
        fig.legend(handles, labels, loc="upper left", bbox_to_anchor=(0.005, top - 0.5 / height),
                   ncols=len(labels), handlelength=1.6)
        header += 0.3
    wrapped = textwrap.fill(caption, width=int(width * 15))
    fig.text(0.01, 0.08 / height, wrapped, ha="left", va="bottom", fontsize=7.5, color=MUTED)
    footer = 0.15 + 0.14 * (wrapped.count("\n") + 1)
    fig.tight_layout(rect=(0, footer / height, 1, 1 - header / height))
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def _caption(source: str, period: str, values: str) -> str:
    return f"Fuente: {source} · Período: {period} · Valores: {values}"


def _department_names(panel: pd.DataFrame) -> dict[int, str]:
    return panel.drop_duplicates("DepartamentoCodigo").set_index("DepartamentoCodigo")["Departamento"].to_dict()


def _spread_labels(values: dict, min_gap: float) -> dict:
    """Separa verticalmente etiquetas directas para que no se superpongan."""
    ordered = sorted(values.items(), key=lambda kv: kv[1])
    placed = {}
    previous = -np.inf
    for key, value in ordered:
        position = max(value, previous + min_gap)
        placed[key] = position
        previous = position
    return placed


def _department_lines(ax, panel: pd.DataFrame, column: str, scale: float = 1.0, label_fmt: str = "{:.2f}"):
    names = _department_names(panel)
    ends = {}
    for code, group in panel.groupby("DepartamentoCodigo"):
        group = group.sort_values("AnioEjercicio")
        y = group[column] / scale
        ax.plot(group["AnioEjercicio"], y, color=DEPARTMENT_COLORS[code], label=names[code],
                marker="o", markersize=4, markeredgecolor=SURFACE, markeredgewidth=1)
        ends[code] = (group["AnioEjercicio"].iloc[-1], y.iloc[-1])
    low, high = ax.get_ylim()
    positions = _spread_labels({c: v for c, (_, v) in ends.items()}, (high - low) * 0.06)
    for code, (x, value) in ends.items():
        ax.annotate(f"{names[code]} {label_fmt.format(value)}", xy=(x, value), xytext=(x + 0.25, positions[code]),
                    fontsize=8, color=TEXT_SECONDARY, va="center",
                    arrowprops=dict(arrowstyle="-", color=AXIS, lw=0.6))
    ax.set_xlim(panel["AnioEjercicio"].min() - 0.3, panel["AnioEjercicio"].max() + 2.4)
    ax.set_xticks(sorted(panel["AnioEjercicio"].unique()))


def _period(panel: pd.DataFrame) -> str:
    return f"ejercicios {panel['AnioEjercicio'].min()}–{panel['AnioEjercicio'].max()} (julio–junio)"


def _annotated_heatmap(ax, matrix: pd.DataFrame, cmap, vmin, vmax, fmt: str):
    image = ax.imshow(matrix.values.astype(float), cmap=cmap, vmin=vmin, vmax=vmax, aspect="auto")
    ax.set_xticks(range(matrix.shape[1]), [str(c) for c in matrix.columns])
    ax.set_yticks(range(matrix.shape[0]), [str(i) for i in matrix.index])
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(False)
    span = vmax - vmin
    for (i, j), value in np.ndenumerate(matrix.values.astype(float)):
        if np.isnan(value):
            continue
        intensity = abs(value - (vmin + vmax) / 2) / (span / 2) if cmap is DIVERGING else (value - vmin) / span
        ax.text(j, i, fmt.format(value), ha="center", va="center", fontsize=7.5,
                color=SURFACE if intensity > 0.6 else TEXT)
    return image


# ---------------------------------------------------------------------------
# 1–2. Cobertura y faltantes climáticos
# ---------------------------------------------------------------------------


def coverage_heatmap(coverage: pd.DataFrame, years: tuple[int, int], path: Path) -> Path:
    data = coverage[coverage["AnioEjercicio"].between(*years)]
    matrix = data.pivot(index="EstacionAgr", columns="AnioEjercicio", values="cobertura_registros") * 100
    fig, ax = plt.subplots(figsize=(10, 3.4))
    _annotated_heatmap(ax, matrix, SEQUENTIAL_BLUE, 90, 100, "{:.1f}")
    ax.set_xlabel("Ejercicio ganadero")
    return _finish(
        fig, "Cobertura climática por estación y ejercicio (%)",
        "Días con temperatura, precipitación y viento sobre días con registro. Escala 90–100 %.",
        _caption(SOURCE_INIA, f"ejercicios {years[0]}–{years[1]}", "observados (conteo de días)"), path,
    )


def missing_heatmap(missing: pd.DataFrame, path: Path) -> Path:
    matrix = missing.pivot_table(index=["EstacionAgr", "variable"], columns="anio", values="dias_faltantes")
    matrix.index = [f"{station} · {var}" for station, var in matrix.index]
    fig, ax = plt.subplots(figsize=(10, 5.6))
    _annotated_heatmap(ax, matrix, SEQUENTIAL_BLUE, 0, max(5, matrix.values.max()), "{:.0f}")
    ax.set_xlabel("Año calendario")
    return _finish(
        fig, "Días faltantes por estación, variable y año (días)",
        "Variables requeridas por el Chill Index. 2026 llega hasta marzo.",
        _caption(SOURCE_INIA, f"{missing['anio'].min()}–{missing['anio'].max()}", "observados (conteo de días)"), path,
    )


# ---------------------------------------------------------------------------
# 3–6. Objetivos
# ---------------------------------------------------------------------------


def target_series(panel: pd.DataFrame, column: str, title: str, ylabel: str, fmt: str, path: Path) -> Path:
    fig, ax = plt.subplots(figsize=(9, 4.6))
    _department_lines(ax, panel, column, label_fmt=fmt)
    ax.set_ylabel(ylabel)
    ax.set_xlabel("Ejercicio ganadero")
    return _finish(fig, title, "Una línea por departamento; etiqueta con el valor del último ejercicio.",
                   _caption(SOURCE_SNIG, _period(panel), "observados, agregados por departamento y ejercicio"), path,
                   legend_from=ax)


def stock_and_deaths(panel: pd.DataFrame, path: Path) -> Path:
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.6))
    _department_lines(axes[0], panel, "stock_ovino", scale=1000, label_fmt="{:.0f}")
    axes[0].set_title("Stock ovino declarado al cierre (miles de animales)", loc="left")
    _department_lines(axes[1], panel, "muertes_ovinas", scale=1000, label_fmt="{:.1f}")
    axes[1].set_title("Muertes ovinas declaradas en el ejercicio (miles de animales)", loc="left")
    for ax in axes:
        ax.set_xlabel("Ejercicio ganadero")
    return _finish(fig, "Stock y muertes ovinas por departamento (miles de animales)",
                   "Numerador y denominador de la tasa proxy de mortalidad, en gráficos separados.",
                   _caption(SOURCE_SNIG, _period(panel), "observados, agregados por departamento y ejercicio"), path,
                   legend_from=axes[0])


def mortality_distribution(panel: pd.DataFrame, path: Path) -> Path:
    names = _department_names(panel)
    order = panel.groupby("DepartamentoCodigo")["tasa_mortalidad_1000"].median().sort_values().index
    fig, ax = plt.subplots(figsize=(9, 3.8))
    for i, code in enumerate(order):
        values = panel.loc[panel["DepartamentoCodigo"] == code, "tasa_mortalidad_1000"]
        ax.scatter(values, np.full(len(values), i), s=45, color=DEPARTMENT_COLORS[code],
                   edgecolors=SURFACE, linewidths=1.5, zorder=3)
        ax.plot([values.min(), values.max()], [i, i], color=AXIS, lw=1, zorder=2)
        median = values.median()
        ax.plot([median, median], [i - 0.25, i + 0.25], color=TEXT, lw=2, zorder=4)
        ax.text(values.max() + 1.5, i, f"mediana {median:.0f}", va="center", fontsize=8, color=TEXT_SECONDARY)
    ax.set_yticks(range(len(order)), [names[c] for c in order])
    ax.set_xlabel("Tasa proxy de mortalidad ovina (muertes por mil)")
    ax.grid(axis="y", visible=False)
    return _finish(fig, "Distribución de la mortalidad ovina por departamento (por mil)",
                   "Cada punto es un ejercicio; la barra negra es la mediana.",
                   _caption(SOURCE_SNIG, _period(panel), "observados, agregados por departamento y ejercicio"), path)


# ---------------------------------------------------------------------------
# 7. Categorías de Chill Index
# ---------------------------------------------------------------------------


def ci_category_bars(category_days: pd.DataFrame, names: dict[int, str], path: Path) -> Path:
    risk = CATEGORY_LABELS[1:]  # "Sin riesgo" domina y oculta el resto
    codes = sorted(category_days["DepartamentoCodigo"].unique())
    fig, axes = plt.subplots(1, len(codes), figsize=(15, 4.2), sharey=True)
    for ax, code in zip(axes, codes):
        data = category_days[category_days["DepartamentoCodigo"] == code].pivot(
            index="AnioEjercicio", columns="ci_categoria", values="dias")
        bottom = np.zeros(len(data))
        for label, color in zip(risk, ORDINAL_BLUE):
            ax.bar(data.index, data[label], bottom=bottom, color=color, width=0.75,
                   edgecolor=SURFACE, linewidth=1, label=label)
            bottom += data[label].values
        ax.set_title(names[code], loc="left")
        ax.set_xticks(data.index, [str(y)[2:] for y in data.index])
        ax.grid(axis="x", visible=False)
    axes[0].set_ylabel("Días en el ejercicio")
    return _finish(fig, "Días con Chill Index en riesgo por ejercicio y departamento (días)",
                   "Categorías INIA: bajo 900–999, medio 1000–1099, alto 1100–1199, críticas ≥ 1200. "
                   "Eje x: ejercicio (’17 = 2016/17).",
                   _caption(SOURCE_INIA, "ejercicios 2017–2025 (julio–junio)", "observados, días agregados por ejercicio"),
                   path, legend_from=axes[0])


# ---------------------------------------------------------------------------
# 8–10. Relaciones clima–mortalidad
# ---------------------------------------------------------------------------


def scatter_by_department(panel: pd.DataFrame, x: str, y: str, xlabel: str, ylabel: str,
                          title: str, path: Path) -> Path:
    names = _department_names(panel)
    codes = sorted(panel["DepartamentoCodigo"].unique())
    fig, axes = plt.subplots(1, len(codes), figsize=(15, 3.9))
    for ax, code in zip(axes, codes):
        group = panel[panel["DepartamentoCodigo"] == code]
        ax.scatter(group[x], group[y], s=50, color=DEPARTMENT_COLORS[code], edgecolors=SURFACE, linewidths=1.5, zorder=3)
        r = np.corrcoef(group[x], group[y])[0, 1] if group[x].std() > 0 else np.nan
        ax.set_title(names[code], loc="left")
        ax.set_title(f"r = {r:.2f} (n = {len(group)})", loc="right", fontsize=8, color=TEXT_SECONDARY)
        ax.set_xlabel(xlabel)
    axes[0].set_ylabel(ylabel)
    return _finish(fig, title,
                   "Un panel por departamento con su propia escala: muestra variación entre años, no entre regiones.",
                   _caption(f"{SOURCE_SNIG} e {SOURCE_INIA}", _period(panel),
                            "observados, agregados por departamento y ejercicio"), path)


# ---------------------------------------------------------------------------
# 11–13. Correlaciones, extremos y ventanas
# ---------------------------------------------------------------------------


def correlation_heatmap(correlations: pd.DataFrame, labels: dict[str, str], target_labels: dict[str, str],
                        window: str, path: Path) -> Path:
    data = correlations[correlations["ventana"].isin([window, "historia"])]
    columns = {}
    for target, short in target_labels.items():
        subset = data[data["objetivo"] == target].set_index("variable")
        columns[f"{short}\nglobal"] = subset["r_global"]
        columns[f"{short}\nintra-depto."] = subset["r_intra_departamento"]
    matrix = pd.DataFrame(columns).loc[list(labels)]
    matrix.index = [labels[v] for v in matrix.index]
    fig, ax = plt.subplots(figsize=(8, 7))
    image = _annotated_heatmap(ax, matrix, DIVERGING, -1, 1, "{:+.2f}")
    ax.xaxis.tick_top()
    fig.colorbar(image, ax=ax, shrink=0.6, label="r de Pearson")
    return _finish(fig, "Correlación de cada variable con los objetivos (r de Pearson)",
                   "Global: 45 obs. (40 para rezagos). Intra-depto.: desvíos respecto de la media de cada departamento.",
                   _caption(f"{SOURCE_SNIG} e {SOURCE_INIA}", "ejercicios 2017–2025, ventana julio–junio",
                            "correlaciones sobre valores observados agregados"), path)


def zscore_heatmap(panel: pd.DataFrame, z: pd.DataFrame, column: str, title: str, path: Path) -> Path:
    data = panel[["Departamento", "AnioEjercicio"]].assign(z=z[column])
    matrix = data.pivot(index="Departamento", columns="AnioEjercicio", values="z")
    fig, ax = plt.subplots(figsize=(10, 3.4))
    image = _annotated_heatmap(ax, matrix, DIVERGING, -2.5, 2.5, "{:+.1f}")
    fig.colorbar(image, ax=ax, shrink=0.8, label="z dentro del departamento")
    ax.set_xlabel("Ejercicio ganadero")
    return _finish(fig, title, "z = (valor − media del departamento) / desvío del departamento. |z| ≥ 1,5 marca un año extremo.",
                   _caption(SOURCE_SNIG, _period(panel), "observados, estandarizados por departamento"), path)


def window_dot_plot(comparison: pd.DataFrame, labels: dict[str, str], target_labels: dict[str, str], path: Path) -> Path:
    variables = list(labels)
    fig, axes = plt.subplots(1, len(target_labels), figsize=(12, 5.2), sharey=True)
    for ax, (target, short) in zip(axes, target_labels.items()):
        data = comparison[comparison["objetivo"] == target].set_index("variable").loc[variables]
        y = np.arange(len(variables))
        for i, (_, row) in enumerate(data.iterrows()):
            ax.plot([row["ejercicio"], row["jul_oct"]], [i, i], color=AXIS, lw=1, zorder=2)
        for window, name in [("ejercicio", "Ejercicio completo"), ("jul_oct", "Julio–octubre")]:
            ax.scatter(data[window], y, s=55, color=WINDOW_COLORS[window], edgecolors=SURFACE,
                       linewidths=1.5, zorder=3, label=name)
        ax.axvline(0, color=TEXT_SECONDARY, lw=0.8)
        ax.set_xlim(-1, 1)
        ax.set_title(short, loc="left")
        ax.set_xlabel("r intra-departamento")
        ax.grid(axis="y", visible=False)
    axes[0].set_yticks(np.arange(len(variables)), [labels[v] for v in variables])
    axes[0].invert_yaxis()
    return _finish(fig, "Ejercicio completo frente a julio–octubre (r de Pearson)",
                   "Correlación intra-departamento de cada variable climática con el objetivo, para las dos ventanas.",
                   _caption(f"{SOURCE_SNIG} e {SOURCE_INIA}", "ejercicios 2017–2025",
                            "correlaciones sobre valores observados agregados"), path, legend_from=axes[0])


# ---------------------------------------------------------------------------
# 14. Observados frente a predicciones fuera de muestra
# ---------------------------------------------------------------------------

REGRESSION_PANELS = {
    "completo": ["R1_promedio_departamental", "ridge_A_ejercicio", "ridge_B_ejercicio"],
    "con_rezago": ["R2_persistencia", "ridge_H_sin_clima", "ridge_C-A_ejercicio", "ridge_C-B_ejercicio"],
}
CLASSIFICATION_PANELS = {
    "completo": ["logistica_A_ejercicio", "logistica_B_ejercicio"],
    "con_rezago": ["C2_persistencia_riesgo", "logistica_H_sin_clima", "logistica_C-A_ejercicio",
                   "logistica_C-B_ejercicio"],
}
SET_LABELS = {"completo": "panel completo, 2017–2025 (45 obs.)", "con_rezago": "panel con rezago, 2018–2025 (40 obs.)"}


def observed_vs_predicted(oof: pd.DataFrame, set_name: str, models: list[str], run_id: str, path: Path) -> Path:
    data = oof[(oof["conjunto"] == set_name) & oof["modelo"].isin(models)]
    low = min(data["y_true"].min(), data["y_pred"].min()) - 0.02
    high = max(data["y_true"].max(), data["y_pred"].max()) + 0.02
    fig, axes = plt.subplots(1, len(models), figsize=(3.6 * len(models), 4.2), sharex=True, sharey=True)
    for ax, model in zip(np.atleast_1d(axes), models):
        group = data[data["modelo"] == model]
        ax.plot([low, high], [low, high], color=AXIS, lw=1, zorder=1)
        ax.scatter(group["y_pred"], group["y_true"], s=40, color=DEPARTMENT_COLORS[2], edgecolors=SURFACE,
                   linewidths=1.5, zorder=3)
        mae = np.mean(np.abs(group["y_true"] - group["y_pred"]))
        ax.set_title(model, loc="left", fontsize=9)
        ax.set_title(f"MAE {mae:.4f}", loc="right", fontsize=8, color=TEXT_SECONDARY)
        ax.set_xlim(low, high)
        ax.set_ylim(low, high)
        ax.set_xlabel("Predicho fuera de muestra (UG/ha)")
    np.atleast_1d(axes)[0].set_ylabel("Observado (UG/ha)")
    return _finish(fig, f"Intensidad ganadera: observado frente a predicho (UG/ha) — {SET_LABELS[set_name]}",
                   "Cada punto es un departamento–ejercicio predicho sin haber visto su año. La diagonal es la predicción perfecta.",
                   _caption(SOURCE_SNIG + " e " + SOURCE_INIA, f"Leave-One-Year-Out · corrida {run_id}",
                            "observados frente a predichos fuera de muestra"), path)


def predicted_probabilities(oof: pd.DataFrame, set_name: str, models: list[str], run_id: str, path: Path) -> Path:
    data = oof[(oof["conjunto"] == set_name) & oof["modelo"].isin(models)]
    fig, axes = plt.subplots(1, len(models), figsize=(3.6 * len(models), 4.2), sharey=True)
    offsets = {code: (i - 2) * 0.12 for i, code in enumerate(sorted(DEPARTMENT_COLORS))}
    for ax, model in zip(np.atleast_1d(axes), models):
        group = data[data["modelo"] == model]
        x = group["AnioEjercicio"] + group["DepartamentoCodigo"].map(offsets)
        for label, color, name in [(0, WINDOW_COLORS["ejercicio"], "Observado: no elevada"),
                                   (1, WINDOW_COLORS["jul_oct"], "Observado: elevada")]:
            mask = group["y_true"] == label
            ax.scatter(x[mask], group.loc[mask, "y_proba"], s=36, color=color, edgecolors=SURFACE,
                       linewidths=1.2, zorder=3, label=name)
        ax.axhline(0.5, color=TEXT_SECONDARY, lw=0.8, ls="--")
        ba = balanced_accuracy_from(group)
        ax.set_title(model, loc="left", fontsize=9)
        ax.set_title(f"BA {ba:.2f}", loc="right", fontsize=8, color=TEXT_SECONDARY)
        ax.set_xticks(sorted(group["AnioEjercicio"].unique()),
                      [str(y)[2:] for y in sorted(group["AnioEjercicio"].unique())])
        ax.set_xlabel("Ejercicio (’18 = 2017/18)")
        ax.set_ylim(-0.05, 1.05)
    np.atleast_1d(axes)[0].set_ylabel("Probabilidad predicha de mortalidad elevada")
    return _finish(fig, f"Mortalidad elevada: probabilidad fuera de muestra — {SET_LABELS[set_name]}",
                   "Cada punto es un departamento–ejercicio; color = clase observada. Línea punteada: corte 0,5.",
                   _caption(SOURCE_SNIG + " e " + SOURCE_INIA, f"Leave-One-Year-Out · corrida {run_id}",
                            "probabilidades predichas fuera de muestra"), path,
                   legend_from=np.atleast_1d(axes)[0])


def balanced_accuracy_from(group: pd.DataFrame) -> float:
    positives = group["y_true"] == 1
    if positives.all() or not positives.any():
        return float("nan")
    return float(((group.loc[positives, "y_pred"] == 1).mean() + (group.loc[~positives, "y_pred"] == 0).mean()) / 2)


def out_of_sample_figures(tables: dict, out_dir: Path, run_id: str) -> list[Path]:
    paths = []
    for set_name, models in REGRESSION_PANELS.items():
        paths.append(observed_vs_predicted(tables["regresion_predicciones"], set_name, models, run_id,
                                           out_dir / f"eda_14_regresion_{set_name}.png"))
    for set_name, models in CLASSIFICATION_PANELS.items():
        paths.append(predicted_probabilities(tables["clasificacion_predicciones"], set_name, models, run_id,
                                             out_dir / f"eda_14_clasificacion_{set_name}.png"))
    return paths
