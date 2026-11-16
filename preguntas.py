import pandas as pd


def responder_preguntas(df: pd.DataFrame) -> None:
    print("\n=== Pregunta 1: programa con mayor tasa de deserción ===")
    p1 = (
        df.groupby("programa", observed=True)
        .agg(tasa=("desertor", "mean"), estudiantes=("desertor", "size"))
        .sort_values("tasa", ascending=False)
    )
    print(p1)
    print(
        f"\nRespuesta: {p1.index[0]} tiene la tasa más alta "
        f"({p1.iloc[0]['tasa']:.1%}) con {int(p1.iloc[0]['estudiantes'])} estudiantes."
    )

    print("\n=== Pregunta 2: deserción según beca ===")
    p2 = (
        df.groupby("beca", observed=True)
        .agg(tasa=("desertor", "mean"), estudiantes=("desertor", "size"))
    )
    print(p2)
    print(
        "\nRespuesta: sí se ve diferencia entre becados y no becados. "
        "Eso no prueba que la beca cause la permanencia: puede ser que "
        "quien recibe beca ya tenía mejores condiciones o motivación."
    )

    print("\n=== Pregunta 3: jornada con menor promedio acumulado ===")
    p3 = (
        df.groupby("jornada", observed=True)
        .agg(
            promedio=("promedio_acumulado", "mean"),
            estudiantes=("promedio_acumulado", "size"),
        )
        .sort_values("promedio")
    )
    print(p3)
    print(
        f"\nRespuesta: {p3.index[0]} tiene el promedio más bajo "
        f"({p3.iloc[0]['promedio']:.2f}) con {int(p3.iloc[0]['estudiantes'])} estudiantes."
    )

    print("\n=== Pregunta 4: materias reprobadas desertores vs activos ===")
    sub = df[df["estado"].isin(["desertor", "activo"])]
    p4 = (
        sub.groupby("estado", observed=True)
        .agg(
            materias_promedio=("materias_reprobadas", "mean"),
            estudiantes=("materias_reprobadas", "size"),
        )
    )
    print(p4)
    print(
        "\nRespuesta: los desertores tienen más materias reprobadas en promedio. "
        "Se excluyen los graduados porque ya no están en ninguno de los dos grupos "
        "que se están comparando."
    )

    print("\n=== Pregunta 5: deserción según cuartil de asistencia ===")
    p5 = (
        df.groupby("cuartil_asistencia", observed=True)
        .agg(
            tasa=("desertor", "mean"),
            asistencia_promedio=("asistencia_pct", "mean"),
            estudiantes=("desertor", "size"),
        )
        .reindex(["Q1", "Q2", "Q3", "Q4"])
    )
    print(p5)
    print(
        "\nRespuesta: la deserción baja cuando sube la asistencia (de Q1 a Q4). "
        "Se ve una asociación clara, pero no prueba causa: puede haber otras "
        "variables (trabajo, motivación, etc.) que muevan las dos cosas a la vez."
    )
