"""Utilidades para escribir reportes en Markdown."""

import pandas as pd


def md_table(df: pd.DataFrame, float_format: str = "{:.3f}") -> str:
    def cell(value) -> str:
        if isinstance(value, float):
            return "" if pd.isna(value) else float_format.format(value)
        return "" if value is None or value is pd.NA else str(value)

    lines = ["| " + " | ".join(map(str, df.columns)) + " |", "|" + "---|" * df.shape[1]]
    lines += ["| " + " | ".join(cell(v) for v in row) + " |" for row in df.itertuples(index=False)]
    return "\n".join(lines)
