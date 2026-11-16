import pandas as pd

from config import registrar


def eliminar_duplicados(df: pd.DataFrame) -> pd.DataFrame:
    antes = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    eliminadas = antes - len(df)
    registrar(
        "eliminar_duplicados",
        "todas",
        "drop_duplicates + reset_index",
        eliminadas,
        "Había filas idénticas. Dejarlas duplicaba el peso de esos estudiantes en cualquier tasa o promedio.",
    )
    return df


def tratar_faltantes(df: pd.DataFrame) -> pd.DataFrame:
    nulos_prom = df["promedio_acumulado"].isna().sum()
    df = df.dropna(subset=["promedio_acumulado"]).reset_index(drop=True)
    registrar(
        "tratar_faltantes",
        "promedio_acumulado",
        "eliminar filas con nulo",
        nulos_prom,
        "Una nota no se puede inventar. Sin promedio el estudiante no aporta al análisis de rendimiento.",
    )

    nulos_ciudad = df["ciudad_procedencia"].isna().sum()
    df["ciudad_procedencia"] = df["ciudad_procedencia"].fillna("Sin dato")
    registrar(
        "tratar_faltantes",
        "ciudad_procedencia",
        "rellenar nulos con 'Sin dato'",
        nulos_ciudad,
        "La ciudad no se puede adivinar, pero tampoco conviene borrar la fila. 'Sin dato' deja constancia de que faltaba.",
    )

    nulos_colegio = df["tipo_colegio"].isna().sum()
    df["tipo_colegio"] = df["tipo_colegio"].fillna("Sin dato")
    registrar(
        "tratar_faltantes",
        "tipo_colegio",
        "rellenar nulos con 'Sin dato'",
        nulos_colegio,
        "Mismo criterio que ciudad: no se inventa el tipo de colegio y no se elimina la fila completa.",
    )

    return df


def tratar_imposibles(df: pd.DataFrame) -> pd.DataFrame:
    fuera_edad = ((df["edad"] < 15) | (df["edad"] > 60)).sum()
    df.loc[(df["edad"] < 15) | (df["edad"] > 60), "edad"] = pd.NA
    mediana_edad = df["edad"].median()
    df["edad"] = df["edad"].fillna(mediana_edad)
    registrar(
        "tratar_imposibles",
        "edad",
        "edades fuera de 15-60 a nulo y luego mediana",
        fuera_edad,
        "Una edad de 12 o de 150 no es creíble en este contexto. La mediana no se deja arrastrar por extremos.",
    )

    fuera_prom = (df["promedio_acumulado"] > 5).sum()
    df.loc[df["promedio_acumulado"] > 5, "promedio_acumulado"] = pd.NA
    nulos_prom = df["promedio_acumulado"].isna().sum()
    df = df.dropna(subset=["promedio_acumulado"]).reset_index(drop=True)
    registrar(
        "tratar_imposibles",
        "promedio_acumulado",
        "promedios > 5 a nulo y eliminar esas filas",
        fuera_prom,
        "La escala es de 0 a 5. Un 78 es un error de registro y distorsiona cualquier promedio institucional.",
    )

    mask_no_trabaja = df["trabaja"].str.lower() == "no"
    n_cero = (mask_no_trabaja & df["horas_trabajo_semana"].isna()).sum()
    df.loc[mask_no_trabaja, "horas_trabajo_semana"] = df.loc[
        mask_no_trabaja, "horas_trabajo_semana"
    ].fillna(0)
    registrar(
        "tratar_imposibles",
        "horas_trabajo_semana",
        "si no trabaja, horas = 0",
        n_cero,
        "Si el estudiante declara que no trabaja, las horas deben ser cero. El nulo anterior era inconsistente.",
    )

    fuera_horas = (df["horas_trabajo_semana"] > 100).sum()
    df.loc[df["horas_trabajo_semana"] > 100, "horas_trabajo_semana"] = pd.NA
    mediana_trabajan = df.loc[
        df["trabaja"].str.lower() == "sí", "horas_trabajo_semana"
    ].median()
    n_mediana = df["horas_trabajo_semana"].isna().sum()
    df["horas_trabajo_semana"] = df["horas_trabajo_semana"].fillna(mediana_trabajan)
    registrar(
        "tratar_imposibles",
        "horas_trabajo_semana",
        "horas > 100 a nulo y luego mediana de quienes trabajan",
        fuera_horas + n_mediana,
        "Más de 100 horas a la semana no es realista. Se usa la mediana de los que sí trabajan para no inventar ceros.",
    )

    return df