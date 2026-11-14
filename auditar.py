import pandas as pd


def auditar(df: pd.DataFrame) -> None:
    """Revisa nulos reales, faltantes disfrazados, valores imposibles,
    duplicados y formatos de fecha.

    Pregunta del taller: ¿cuál de estos problemas afecta más el análisis? ¿Por qué?
    """
    print("\n--- nulos reales ---")
    print(df.isnull().sum())

    guion_asistencia = (df["asistencia_pct"].astype(str) == "-").sum()
    guion_horas = (df["horas_trabajo_semana"].astype(str) == "-").sum()
    distancia_999 = (df["distancia_km"] == 999).sum()
    print("\n--- faltantes disfrazados ---")
    print(f"asistencia_pct con '-': {guion_asistencia}")
    print(f"horas_trabajo_semana con '-': {guion_horas}")
    print(f"distancia_km en 999: {distancia_999}")

    con_porcentaje = df["asistencia_pct"].astype(str).str.contains("%", regex=False).sum()
    print(f"\nasistencia_pct con signo %: {con_porcentaje}")

    duplicadas = df.duplicated().sum()
    print(f"\nfilas duplicadas: {duplicadas}")

    edad_fuera = ((df["edad"] < 15) | (df["edad"] > 60)).sum()
    promedio_mayor_5 = (df["promedio_acumulado"] > 5).sum()
    print("\n--- valores imposibles ---")
    print(f"edad fuera de 15 a 60: {edad_fuera}")
    print(f"promedio mayor a 5: {promedio_mayor_5}")

    fechas = df["fecha_matricula"].astype(str)
    formato_iso = fechas.str.match(r"^\d{4}-\d{2}-\d{2}$").sum()
    formato_dmy = fechas.str.match(r"^\d{2}/\d{2}/\d{4}$").sum()
    print("\n--- fechas ---")
    print(f"formato AAAA-MM-DD: {formato_iso}")
    print(f"formato DD/MM/AAAA: {formato_dmy}")

    print(
        "\nPregunta del taller: ¿cuál de estos problemas afecta más el análisis? ¿Por qué?"
        "\n"
        "Lo que más afecta el análisis son los promedios mayores a 5. "
        "Un 78 en una escala de 0 a 5 sube el promedio de toda la institución. "
    )
