import pandas as pd

from config import VALIDOS, registrar


def convertir_numericos(df: pd.DataFrame) -> pd.DataFrame:
    asistencia = df["asistencia_pct"].astype(str)
    con_porcentaje = asistencia.str.contains("%", regex=False).sum()
    guiones_asistencia = (asistencia == "-").sum()
    df["asistencia_pct"] = (
        asistencia.str.replace("%", "", regex=False)
        .replace("-", pd.NA)
        .pipe(pd.to_numeric, errors="coerce")
    )
    registrar(
        "convertir_numericos",
        "asistencia_pct",
        "quitar % y convertir a número; '-' a nulo",
        con_porcentaje + guiones_asistencia,
        "La columna venía como texto por el signo % y los guiones. Sin convertirla no se pueden calcular promedios ni cuartiles.",
    )

    horas = df["horas_trabajo_semana"].astype(str)
    guiones_horas = (horas == "-").sum()
    df["horas_trabajo_semana"] = horas.replace("-", pd.NA).pipe(
        pd.to_numeric, errors="coerce"
    )
    registrar(
        "convertir_numericos",
        "horas_trabajo_semana",
        "convertir a número; '-' a nulo",
        guiones_horas,
        "El guion impedía tratar la columna como numérica. Quienes no trabajan ya tienen 0, así que el guion se interpreta como dato faltante.",
    )

    distancias_999 = (df["distancia_km"] == 999).sum()
    df.loc[df["distancia_km"] == 999, "distancia_km"] = pd.NA
    registrar(
        "convertir_numericos",
        "distancia_km",
        "999 a nulo",
        distancias_999,
        "999 no es una distancia real. Se usa como código de faltante y distorsiona cualquier promedio.",
    )

    return df


def unificar_categorias(df: pd.DataFrame) -> pd.DataFrame:
    mapa_programa = {
        "psicologia": "Psicología",
        "ingenieria de sistemas": "Ingeniería de Sistemas",
    }
    antes = df["programa"].copy()
    temp = df["programa"].astype(str).str.strip().str.lower()
    temp = temp.replace(mapa_programa)
    df["programa"] = temp.replace(
        {
            "administración de empresas": "Administración de Empresas",
            "administracion de empresas": "Administración de Empresas",
            "contaduría pública": "Contaduría Pública",
            "contaduria publica": "Contaduría Pública",
            "derecho": "Derecho",
            "psicología": "Psicología",
            "psicologia": "Psicología",
            "ingeniería de sistemas": "Ingeniería de Sistemas",
            "ingenieria de sistemas": "Ingeniería de Sistemas",
            "ingeniería industrial": "Ingeniería Industrial",
            "ingenieria industrial": "Ingeniería Industrial",
            "enfermería": "Enfermería",
            "enfermeria": "Enfermería",
            "diseño gráfico": "Diseño Gráfico",
            "diseno grafico": "Diseño Gráfico",
            "diseño grafico": "Diseño Gráfico",
        }
    )
    filas = (antes != df["programa"]).sum()
    registrar(
        "unificar_categorias",
        "programa",
        "strip + lower + replace de variantes",
        filas,
        "Había variantes tipográficas (Psicologia / Psicología, Ingenieria de Sistemas). Sin unificar, los conteos se parten y las tasas salen mal.",
    )

    mapa_jornada = {
        "diurna": "Diurna",
        "nocturna": "Nocturna",
        "fin de semana": "Fin de semana",
    }
    antes_j = df["jornada"].copy()
    df["jornada"] = (
        df["jornada"].astype(str).str.strip().str.lower().replace(mapa_jornada)
    )
    filas_j = (antes_j != df["jornada"]).sum()
    registrar(
        "unificar_categorias",
        "jornada",
        "strip + lower + replace",
        filas_j,
        "Aparecían minúsculas y mayúsculas distintas. Se unifican a la forma canónica de VALIDOS.",
    )

    mapa_genero = {
        "f": "Femenino",
        "m": "Masculino",
        "femenino": "Femenino",
        "masculino": "Masculino",
    }
    antes_g = df["genero"].copy()
    df["genero"] = (
        df["genero"].astype(str).str.strip().str.lower().replace(mapa_genero)
    )
    filas_g = (antes_g != df["genero"]).sum()
    registrar(
        "unificar_categorias",
        "genero",
        "strip + lower + replace de F/M y minúsculas",
        filas_g,
        "Había códigos cortos (F/M) y minúsculas. Se deja solo Femenino y Masculino.",
    )

    mapa_ciudad = {
        "bogotá": "Bogotá",
        "bogota": "Bogotá",
        "medellín": "Medellín",
        "medellin": "Medellín",
        "cali": "Cali",
        "bucaramanga": "Bucaramanga",
        "rionegro": "Rionegro",
        "barranquilla": "Barranquilla",
        "otra ciudad": "Otra ciudad",
    }
    antes_c = df["ciudad_procedencia"].copy()
    df["ciudad_procedencia"] = (
        df["ciudad_procedencia"]
        .astype(str)
        .str.strip()
        .str.lower()
        .replace(mapa_ciudad)
    )
    filas_c = (antes_c != df["ciudad_procedencia"]).sum()
    registrar(
        "unificar_categorias",
        "ciudad_procedencia",
        "strip + lower + replace de acentos y mayúsculas",
        filas_c,
        "Bogotá, Medellín y otras ciudades aparecían con y sin tilde, en mayúsculas y minúsculas. Se unifican.",
    )

    return df


def convertir_fechas(df: pd.DataFrame) -> pd.DataFrame:
    fechas = df["fecha_matricula"].astype(str)
    n_iso = fechas.str.match(r"^\d{4}-\d{2}-\d{2}$").sum()
    n_dmy = fechas.str.match(r"^\d{2}/\d{2}/\d{4}$").sum()

    df["fecha_matricula"] = pd.to_datetime(
        df["fecha_matricula"], format="mixed", dayfirst=True, errors="coerce"
    )

    registrar(
        "convertir_fechas",
        "fecha_matricula",
        "unificar AAAA-MM-DD y DD/MM/AAAA a datetime",
        n_iso + n_dmy,
        "Había dos formatos distintos. Al convertir a datetime se puede ordenar y filtrar por fecha sin errores.",
    )

    return df
