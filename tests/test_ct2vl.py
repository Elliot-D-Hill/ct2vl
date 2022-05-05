from numpy import allclose
from pytest import fixture
from ct2vl.ct2vl import CT2VL
from tests import cases

LOD = 100.0
CT_AT_LOD = 37.83

@fixture
def dummy_converter(tmp_path):
    cases.main_calibrate_input.to_csv(f'{tmp_path}/infile', index=False)
    return CT2VL(f'{tmp_path}/infile')

def test_calibrate(dummy_converter):
    dummy_converter.max_replication_rate = cases.calibrate_input[0]
    dummy_converter.max_replication_rate_cycle = cases.calibrate_input[1]
    dummy_converter.calibrate()
    assert allclose(dummy_converter.model['linearregression'].coef_, cases.calibrate_output)

def test_ct_to_viral_load(dummy_converter):
    dummy_converter.model.coef_ = cases.calibrate_output
    viral_load = dummy_converter.ct_to_viral_load(cases.ct_to_viral_load_input, LoD=LOD, Ct_at_LoD=CT_AT_LOD)
    assert allclose(cases.ct_to_viral_load_output, viral_load)

def test_preprocess_traces(dummy_converter):
    dummy_converter.traces = cases.preprocess_traces_input
    dummy_converter.preprocess_traces()
    assert allclose(dummy_converter.traces, cases.preprocess_traces_output)

def test_get_max_replication_rate(dummy_converter):
    dummy_converter.traces = cases.get_max_replication_rate_input
    dummy_converter.get_max_replication_rate()
    assert allclose(dummy_converter.max_replication_rate_cycle, cases.get_max_replication_rate_output[0])
    assert allclose(dummy_converter.max_replication_rate, cases.get_max_replication_rate_output[1])
