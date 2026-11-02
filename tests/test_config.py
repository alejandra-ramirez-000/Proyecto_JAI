from src.config import load_config, project_path


def test_departamentos_y_estaciones():
    cfg = load_config()
    assert sorted(cfg["departments"]) == [2, 4, 15, 18, 19]
    assert cfg["departments"][18]["station"] == "Tacuarembó La Magnolia"
    estaciones = {d["station"] for d in cfg["departments"].values()}
    assert not estaciones & set(cfg["excluded_stations"])


def test_periodo_principal():
    cfg = load_config()
    years = cfg["project"]["end_year"] - cfg["project"]["start_year"] + 1
    assert years == cfg["expected_panel"]["exercises"] == 9
    assert cfg["expected_panel"]["rows"] == years * len(cfg["departments"])


def test_rutas_raw_existen():
    cfg = load_config()
    for key in ["raw_inia", "raw_animales", "raw_generales",
                "catalogo_departamentos", "catalogo_especies"]:
        assert project_path(cfg["paths"][key]).is_file(), key
