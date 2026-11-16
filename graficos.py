from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from config import GRAFICOS


def grafico_faltantes(df: pd.DataFrame) -> None:
    GRAFICOS.mkdir(parents=True, exist_ok=True)

    nulos = df.isnull().sum()
    nulos = nulos[nulos > 0].sort_values(ascending=True)

    plt.figure(figsize=(10, 5))
    nulos.plot(kind="barh", color="steelblue")
    plt.title("Cantidad de valores faltantes por columna")
    plt.xlabel("Número de nulos")
    plt.tight_layout()
    plt.savefig(GRAFICOS / "01_faltantes.png", dpi=120)
    plt.close()


def grafico_distribuciones(original: pd.DataFrame, limpio: pd.DataFrame) -> None:
    GRAFICOS.mkdir(parents=True, exist_ok=True)
    fig, ejes = plt.subplots(2, 2, figsize=(12, 8))

    sns.boxplot(y=original["promedio_acumulado"], ax=ejes[0, 0], color="lightcoral")
    ejes[0, 0].set_title("promedio_acumulado (antes)")

    sns.boxplot(y=original["edad"], ax=ejes[0, 1], color="lightcoral")
    ejes[0, 1].set_title("edad (antes)")

    sns.boxplot(y=limpio["promedio_acumulado"], ax=ejes[1, 0], color="lightgreen")
    ejes[1, 0].set_title("promedio_acumulado (después)")

    sns.boxplot(y=limpio["edad"], ax=ejes[1, 1], color="lightgreen")
    ejes[1, 1].set_title("edad (después)")

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
