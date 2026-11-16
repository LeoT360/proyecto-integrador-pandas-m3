import pandas as pd

from config import registrar


def crear_variables(df: pd.DataFrame) -> pd.DataFrame:
    df["desertor"] = df["estado"].eq("desertor")
    n_desertores = df["desertor"].sum()
    registrar(
        "crear_variables",
        "desertor",
        "True si estado == 'desertor'",
        n_desertores,
        "Convierte el estado en una columna booleana para poder calcular tasas con mean().",
    )

    nulos_asist = df["asistencia_pct"].isna().sum()
    df["cuartil_asistencia"] = pd.qcut(
        df["asistencia_pct"],
        q=4,
        labels=["Q1", "Q2", "Q3", "Q4"],
    )
    registrar(
        "crear_variables",
        "cuartil_asistencia",
        "qcut en 4 grupos de tamaño parecido",
        len(df) - nulos_asist,
        "Los cuartiles agrupan por ranking de asistencia. Así se puede ver si la deserción sube cuando baja la asistencia, sin depender de cortes arbitrarios.",
    )

    return df
