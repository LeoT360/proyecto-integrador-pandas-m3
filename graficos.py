"""Gráficos del taller (mapa de faltantes, boxplots, tasas)."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from config import GRAFICOS


def grafico_faltantes(df: pd.DataFrame) -> None:
    """Mapa de calor de valores faltantes."""
    # TODO 10
    pass


def grafico_distribuciones(original: pd.DataFrame, limpio: pd.DataFrame) -> None:
    """Boxplots antes y después de la limpieza."""
    # TODO 11
    pass


def grafico_tasa_programa(df: pd.DataFrame) -> None:
    """Tasa de deserción por programa."""
    # TODO 12
    pass


def grafico_tasa_asistencia(df: pd.DataFrame) -> None:
    """Tasa de deserción por cuartil de asistencia."""
    # TODO 13
    pass
