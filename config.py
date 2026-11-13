"""Configuración global del proyecto: rutas, constantes y registro de decisiones."""

from pathlib import Path

import pandas as pd

# Opciones de visualización de pandas
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 30)

# Rutas del proyecto
BASE_DIR = Path(__file__).parent
RAW = BASE_DIR / "Data" / "raw" / "datos_estudiantes.csv"
PROCESSED = BASE_DIR / "Data" / "processed"
GRAFICOS = PROCESSED / "graficos"

# Valores válidos de cada columna categórica (la forma correcta de escribirlos).
VALIDOS = {
    "programa": [
        "Administración de Empresas",
        "Contaduría Pública",
        "Derecho",
        "Psicología",
        "Ingeniería de Sistemas",
        "Ingeniería Industrial",
        "Enfermería",
        "Diseño Gráfico",
    ],
    "jornada": ["Diurna", "Nocturna", "Fin de semana"],
    "genero": ["Femenino", "Masculino"],
    "ciudad_procedencia": [
        "Bogotá",
        "Medellín",
        "Cali",
        "Bucaramanga",
        "Rionegro",
        "Barranquilla",
        "Otra ciudad",
    ],
}

# Lista global donde se guardan las decisiones de limpieza
DECISIONES = []


def registrar(paso, columna, accion, filas, justificacion):
    """Guarda una decisión para la tabla de decisiones."""
    DECISIONES.append(
        {
            "paso": paso,
            "columna": columna,
            "accion": accion,
            "filas_afectadas": int(filas),
            "justificacion": justificacion,
        }
    )
