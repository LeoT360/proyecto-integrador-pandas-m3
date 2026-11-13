"""Pasos 3, 4 y 5: conversión de numéricos, unificación de categorías y fechas."""

import pandas as pd

from config import VALIDOS, registrar


def convertir_numericos(df: pd.DataFrame) -> pd.DataFrame:
    """Paso 3: columnas que deberían ser numéricas pero llegan como texto.

    Pistas: quitar %, reemplazar '-', to_numeric, 999 → nulo.
    """
    # TODO 3
    return df


def unificar_categorias(df: pd.DataFrame) -> pd.DataFrame:
    """Paso 4: errores tipográficos en columnas categóricas.

    Pistas: strip + lower + replace con diccionario usando VALIDOS.
    """
    # TODO 4
    return df


def convertir_fechas(df: pd.DataFrame) -> pd.DataFrame:
    """Paso 5: fechas escritas en dos formatos (AAAA-MM-DD y DD/MM/AAAA)."""
    # TODO 5
    return df
