from numpy import allclose, log, exp
from ct2vl.ct2vl import CT2VL, calibrate, fit_model, format_results, preprocess_traces, get_max_efficiency
import cases

CT_AT_LOD = 37.96
LOD = 100.0
CT = 25.0
SLOPE = -0.006
INTERCEPT = 1.0

def ct2vl_alternate_derivation(ct, intercept, slope, ctl, vl):
    intercept = slope + (intercept + 1) 
    log_v = log(vl) + (ctl - 1 + intercept / slope) * log(slope * (ctl - 1) + intercept) - (ct - 1 + intercept / slope) * log(slope * (ct - 1) + intercept)  + ct - ctl
    return exp(log_v)

def test_ct_to_viral_load():
    alternate_viral_load = ct2vl_alternate_derivation(CT, INTERCEPT, SLOPE, CT_AT_LOD, LOD)
    converter = CT2VL(LOD, CT_AT_LOD)
    converter.slopes = SLOPE
    converter.intercepts = INTERCEPT
    viral_load = converter.ct_to_viral_load(CT)
    assert allclose(alternate_viral_load, viral_load)

def test_preprocess_traces():
    processed_traces = preprocess_traces(cases.preprocess_traces_input)
    assert allclose(processed_traces, cases.preprocess_traces_output)

def test_get_max_efficiency():

    max_efficiency = get_max_efficiency(cases.get_max_efficiency_input)
    assert allclose(max_efficiency, cases.get_max_efficiency_output)

def test_fit_model():
    model_fit = fit_model(*cases.fit_model_input)
    assert allclose(model_fit, cases.fit_model_output)

def test_calibrate():
    calibration = calibrate(cases.calibrate_input)
    assert allclose(calibration, cases.calibrate_output)

def test_format_results():
    formatted_results = format_results(*cases.format_results_input)
    assert allclose(formatted_results, cases.format_results_output)
