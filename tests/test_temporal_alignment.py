"""Tests de alineación temporal y rezagos (sección 27.2)."""

import numpy as np
import pandas as pd
import pytest

from src.data.build_panel import LAG_COLUMNS, add_lags
from src.data.load_inia import exercise_year


@pytest.mark.parametrize(
    "fecha, ejercicio",
    [
        ("2020-03-15", 2020),
        ("2020-06-30", 2020),
        ("2020-07-01", 2021),
        ("2020-10-20", 2021),
        ("2021-06-30", 2021),
        ("2020-12-31", 2021),
        ("2021-01-01", 2021),
    ],
)
def test_ejercicio_ganadero(fecha, ejercicio):
    assert exercise_year(pd.Series(pd.to_datetime([fecha])))[0] == ejercicio


def test_ejercicio_2016_incompleto_en_inia(inia):
    ejercicios = pd.Series(exercise_year(inia["Fecha"]), index=inia.index)
    primer_dia_2016 = inia.loc[ejercicios == 2016, "Fecha"].min()
    assert primer_dia_2016 > pd.Timestamp("2015-07-01")


def test_rezagos_respetan_departamento_y_no_usan_futuro(panel):
    indexed = panel.set_index(["DepartamentoCodigo", "AnioEjercicio"])
    for (dep, year), row in indexed.iterrows():
        for col, lag_col in LAG_COLUMNS.items():
            if (dep, year - 1) in indexed.index:
                assert row[lag_col] == indexed.loc[(dep, year - 1), col]
            else:
                assert np.isnan(row[lag_col])


def test_primer_ejercicio_sin_rezago(panel, cfg):
    first = panel[panel["AnioEjercicio"] == cfg["project"]["start_year"]]
    assert first[list(LAG_COLUMNS.values())].isna().all().all()


def test_rezago_faltante_si_falta_el_anio_anterior():
    df = pd.DataFrame(
        {
            "DepartamentoCodigo": [2, 2, 4, 4],
            "AnioEjercicio": [2018, 2020, 2018, 2019],
            **{col: [1.0, 2.0, 3.0, 4.0] for col in LAG_COLUMNS},
        }
    )
    out = add_lags(df.sample(frac=1, random_state=0))
    lag = out.set_index(["DepartamentoCodigo", "AnioEjercicio"])["intensidad_lag1"]
    assert np.isnan(lag[(2, 2020)])  # 2019 ausente: no se usa 2018
    assert lag[(4, 2019)] == 3.0  # no mezcla departamentos
