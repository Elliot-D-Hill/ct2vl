from numpy import allclose
from pytest import fixture
from ct2vl.conversion import Converter
from tests import cases

LOD = 100.0
CT_AT_LOD = 37.83


@fixture
def dummy_converter(tmp_path):
    cases.main_calibrate_input.to_csv(f"{tmp_path}/infile", index=False)
    return Converter(traces=f"{tmp_path}/infile", LoD=LOD, Ct_at_LoD=CT_AT_LOD)


def test_calibrate(dummy_converter):
    dummy_converter.max_replication_rate = cases.calibrate_input[0]
    dummy_converter.max_replication_rate_cycle = cases.calibrate_input[1]
    dummy_converter.calibrate()
    assert allclose(
        dummy_converter.model["linearregression"].coef_, cases.calibrate_output
    )


def test_ct_to_viral_load(dummy_converter):
    dummy_converter.model.coef_ = cases.calibrate_output
    viral_load = dummy_converter.ct_to_viral_load(cases.ct_to_viral_load_input)
    assert allclose(cases.ct_to_viral_load_output, viral_load)


