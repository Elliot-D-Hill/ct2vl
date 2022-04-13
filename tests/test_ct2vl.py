from numpy import allclose
from pickle import dump, load
from ct2vl.ct2vl import CT2VL, fit_model, format_results, preprocess_traces, get_max_efficiency
from tests import cases
from tests.utils import ct2vl_alternate_derivation, make_dummy_converter

CT = 25.0
CT_AT_LOD = 37.96
LOD = 100.0
INTERCEPT = 1.0
SLOPE = -0.006
CONVERTER = make_dummy_converter(LOD, CT_AT_LOD, INTERCEPT, SLOPE)

def test_calibrate(tmp_path):
    filepath = tmp_path / 'test.csv'
    cases.calibrate_input.to_csv(filepath, index=False)
    test_converter = make_dummy_converter(LOD, CT_AT_LOD, cases.calibrate_output[0], cases.calibrate_output[1])
    converter = CT2VL(LOD, CT_AT_LOD)
    converter.calibrate(filepath)
    assert allclose(test_converter.intercepts, converter.intercepts)
    assert allclose(test_converter.slopes, converter.slopes)

def test_ct_to_viral_load():
    alternate_viral_load = ct2vl_alternate_derivation(CT, INTERCEPT, SLOPE, CT_AT_LOD, LOD)
    viral_load = CONVERTER.ct_to_viral_load(CT)
    assert allclose(alternate_viral_load, viral_load)

def test_save(tmp_path):
    filepath = tmp_path / 'test.pkl'
    CONVERTER.save(filepath)
    with open(filepath, 'rb') as f:
        test_converter = load(f)
    assert CONVERTER == test_converter

def test_load(tmp_path):
    filepath = tmp_path / 'test.pkl'
    with open(filepath, 'wb') as f:
        dump(CONVERTER, f)
    test_converter = CT2VL.load(filepath)
    assert CONVERTER == test_converter

def test_preprocess_traces():
    processed_traces = preprocess_traces(cases.preprocess_traces_input)
    assert allclose(processed_traces, cases.preprocess_traces_output)

def test_get_max_efficiency():

    max_efficiency = get_max_efficiency(cases.get_max_efficiency_input)
    assert allclose(max_efficiency, cases.get_max_efficiency_output)

def test_fit_model():
    model_fit = fit_model(*cases.fit_model_input)
    assert allclose(model_fit, cases.fit_model_output)

def test_format_results():
    formatted_results = format_results(*cases.format_results_input)
    assert allclose(formatted_results, cases.format_results_output)
