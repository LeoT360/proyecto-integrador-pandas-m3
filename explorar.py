import pandas as pd


DICCIONARIO = [
    ("id_estudiante", "texto", "identificación", "Código que distingue a cada estudiante. No se usa para promediar."),
    ("programa", "categórica", "explicativa", "Carrera en la que está matriculado."),
    ("facultad", "categórica", "explicativa", "Facultad a la que pertenece el programa."),
    ("jornada", "categórica", "explicativa", "Horario de estudio: diurna, nocturna o fin de semana."),
    ("semestre", "numérica", "explicativa", "Semestre que está cursando."),
    ("promedio_acumulado", "numérica", "explicativa", "Promedio de notas. La escala esperada es de 0 a 5."),
    ("creditos_aprobados", "numérica", "explicativa", "Créditos que ya aprobó."),
    ("materias_reprobadas", "numérica", "explicativa", "Cantidad de materias que ha perdido."),
    ("asistencia_pct", "texto", "explicativa", "Porcentaje de asistencia. Llega como texto por el signo % o el guion."),
    ("sesiones_tutoria", "numérica", "explicativa", "Veces que fue a tutoría."),
    ("cambios_programa", "numérica", "explicativa", "Si cambió de programa (0 o 1)."),
    ("estrato", "categórica", "explicativa", "Estrato socioeconómico, de 1 a 6."),
    ("beca", "categórica", "explicativa", "Si recibe beca: sí o no."),
    ("trabaja", "categórica", "explicativa", "Si trabaja mientras estudia: sí o no."),
    ("horas_trabajo_semana", "texto", "explicativa", "Horas que trabaja a la semana. Llega como texto por el guion."),
    ("distancia_km", "numérica", "explicativa", "Kilómetros entre la casa y la institución."),
    ("edad", "numérica", "explicativa", "Edad del estudiante en años."),
    ("genero", "categórica", "explicativa", "Género registrado."),
    ("ciudad_procedencia", "categórica", "explicativa", "Ciudad de donde viene."),
    ("tipo_colegio", "categórica", "explicativa", "Si el colegio de origen fue público o privado."),
    ("fecha_matricula", "fecha", "explicativa", "Fecha en la que se matriculó."),
    ("estado", "categórica", "resultado", "Situación actual: activo, graduado o desertor."),
    ("motivo_retiro", "categórica", "resultado", "Por qué se fue. Solo aparece cuando ya desertó."),
]


def explorar(df: pd.DataFrame) -> None:
    """Muestra shape, info, describe y value_counts de columnas clave.

    Pregunta del taller: ¿alguna columna numérica aparece como texto? ¿Por qué?
    """
    print(f"Filas: {df.shape[0]} | Columnas: {df.shape[1]}")

    print("\n--- info ---")
    df.info()

    print("\n--- describe ---")
    print(df.describe())

    for columna in ("programa", "jornada", "genero", "estado"):
        print(f"\n--- {columna} ---")
        print(df[columna].value_counts(dropna=False))

    print("\n--- diccionario ---")
    print(f"{'columna':<24} {'tipo':<12} {'rol':<16} descripción")
    for columna, tipo, rol, descripcion in DICCIONARIO:
        print(f"{columna:<24} {tipo:<12} {rol:<16} {descripcion}")

    print(
        "\nPregunta del taller: ¿alguna columna numérica aparece como texto? ¿Por qué?"
        "\n"
        "R: Sí, asistencia_pct y horas_trabajo_semana aparecen como texto. "
        "Traen un guion cuando el dato falta, y la asistencia a veces trae el signo %. "
        "Pandas no puede calcular con eso, así que las deja como texto."
    )
