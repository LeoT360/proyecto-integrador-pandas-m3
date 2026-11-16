from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from config import GRAFICOS


def grafico_faltantes(df: pd.DataFrame) -> None:
    GRAFICOS.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(12, 6))
    sns.heatmap(df.isnull(), cbar=False, yticklabels=False)
    plt.title("Mapa de valores faltantes")
    plt.tight_layout()
    plt.savefig(GRAFICOS / "01_faltantes.png", dpi=120)
    plt.close()


def grafico_distribuciones(original: pd.DataFrame, limpio: pd.DataFrame) -> None:
    GRAFICOS.mkdir(parents=True, exist_ok=True)
    fig, ejes = plt.subplots(2, 2, figsize=(12, 8))

    columnas = ["promedio_acumulado", "edad"]
    for i, col in enumerate(columnas):
        sns.boxplot(y=original[col], ax=ejes[0, i], color="lightcoral")
        ejes[0, i].set_title(f"{col} (antes)")
        sns.boxplot(y=limpio[col], ax=ejes[1, i], color="lightgreen")
        ejes[1, i].set_title(f"{col} (después)")

    plt.tight_layout()
    plt.savefig(GRAFICOS / "02_distribuciones.png", dpi=120)
    plt.close()


def grafico_tasa_programa(df: pd.DataFrame) -> None:
    GRAFICOS.mkdir(parents=True, exist_ok=True)
    tasa = (
        df.groupby("programa", observed=True)["desertor"]
        .mean()
        .sort_values(ascending=False)
    )
    plt.figure(figsize=(10, 5))
    tasa.plot(kind="bar", color="steelblue")
    plt.title("Tasa de deserción por programa")
    plt.ylabel("Proporción de desertores")
    plt.xlabel("")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(GRAFICOS / "03_tasa_programa.png", dpi=120)
    plt.close()


def grafico_tasa_asistencia(df: pd.DataFrame) -> None:
    GRAFICOS.mkdir(parents=True, exist_ok=True)
    tasa = (
        df.groupby("cuartil_asistencia", observed=True)["desertor"]
        .mean()
        .reindex(["Q1", "Q2", "Q3", "Q4"])
    )
    plt.figure(figsize=(8, 5))
    tasa.plot(kind="bar", color="darkorange")
    plt.title("Tasa de deserción por cuartil de asistencia")
    plt.ylabel("Proporción de desertores")
    plt.xlabel("Cuartil de asistencia")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(GRAFICOS / "04_tasa_asistencia.png", dpi=120)
    plt.close()