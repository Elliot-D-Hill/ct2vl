from numpy import allclose, array
from pytest import fixture
from ct2vl.ct2vl import CT2VL, preprocess_traces, get_max_rho
from tests import cases
from pathlib import Path

CT = 25.0
CT_AT_LOD = 37.96
LOD = 100.0
INTERCEPT = 2.0
SLOPE = array([-0.004])

def make_dummy_converter(infile, lod, ct_at_lod, intercept, slope):
    converter = CT2VL(infile, lod, ct_at_lod)
    converter.model.intercept_ = intercept
    converter.model.coef_ = slope
    return converter

@fixture
def dummy_converter(tmp_path):
    Path(f'{tmp_path}/infile').write_text('1,2,3,4,5\n1,2,3,4,5')
    return make_dummy_converter(f'{tmp_path}/infile', LOD, CT_AT_LOD, INTERCEPT, SLOPE)

def test_calibrate(dummy_converter):
    print(cases.calibrate_input[0].shape)
    dummy_converter.calibrate(X=cases.calibrate_input[0].reshape(-1, 1), y=cases.calibrate_input[1])
    assert allclose(dummy_converter.model.intercept_ , cases.calibrate_output[0])
    assert allclose(dummy_converter.model.coef_, cases.calibrate_output[1])

def test_ct_to_viral_load(dummy_converter):
    viral_load = dummy_converter.ct_to_viral_load(cases.ct_to_viral_load_input)
    print(viral_load, cases.ct_to_viral_load_output)
    assert allclose(cases.ct_to_viral_load_output, viral_load)

def test_preprocess_traces():
    processed_traces = preprocess_traces(cases.preprocess_traces_input)
    assert allclose(processed_traces, cases.preprocess_traces_output)

def test_get_max_rho():
    max_efficiency = get_max_rho(cases.get_max_efficiency_input)
    print(max_efficiency)
    assert allclose(max_efficiency, cases.get_max_efficiency_output)
