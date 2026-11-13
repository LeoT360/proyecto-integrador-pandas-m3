"""Paso 11: guardar dataset limpio y tabla de decisiones."""

import pandas as pd

from config import DECISIONES, PROCESSED


def guardar(df: pd.DataFrame) -> None:
    """Guarda dataset_limpio.csv y decisiones.csv."""
    PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED / "dataset_limpio.csv", index=False)
    pd.DataFrame(DECISIONES).to_csv(PROCESSED / "decisiones.csv", index=False)
    print(f"\nDataset limpio guardado: {df.shape[0]} filas, {df.shape[1]} columnas.")
