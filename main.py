"""Punto de entrada del taller de calidad de datos para retención estudiantil."""

import pandas as pd

from config import DECISIONES, RAW
from explorar import explorar
from auditar import auditar
from limpieza import convertir_numericos, unificar_categorias, convertir_fechas
from tratamiento import eliminar_duplicados, tratar_faltantes, tratar_imposibles
from variables import crear_variables
from graficos import (
    grafico_faltantes,
    grafico_distribuciones,
    grafico_tasa_programa,
    grafico_tasa_asistencia,
)
from preguntas import responder_preguntas
from guardar import guardar


def main():
    original = pd.read_csv(RAW)
    df = original.copy()

    # Paso 1
    explorar(df)

    # Paso 2
    auditar(df)
    grafico_faltantes(df)

    # Pasos 3-5
    df = convertir_numericos(df)
    df = unificar_categorias(df)
    df = convertir_fechas(df)

    # Pasos 6-8
    df = eliminar_duplicados(df)
    df = tratar_faltantes(df)
    df = tratar_imposibles(df)

    # Paso 9
    df = crear_variables(df)

    # Gráficos y análisis
    grafico_distribuciones(original, df)
    grafico_tasa_programa(df)
    grafico_tasa_asistencia(df)

    # Paso 10
    responder_preguntas(df)

    print("\nTabla de decisiones:")
    print(pd.DataFrame(DECISIONES))

    # Paso 11
    guardar(df)


if __name__ == "__main__":
    main()
