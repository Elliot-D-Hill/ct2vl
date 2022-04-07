from numpy import log, exp, isclose, array_equal
from pandas import DataFrame, Series
from ct2vl.ct2vl import preprocess_traces, get_max_efficiency, ct_value_to_viral_load


def test_preprcess_traces():
    input_case = DataFrame({
        0: [1, 1, 0],
        1: [2, 2, 0],
        2: [3, 3, 0],
        3: [-1, 1, 0],
        4: [2, -2, 0],
        5: [1, 1, 1],
        6: [3, 2, 1]
    })
    output_case = DataFrame({
        0: [1, 3, 3, 4],
        1: [2, 2, 2, 3],
        2: [1, 1, 2, 2]
    })
    processed_traces = preprocess_traces(input_case)
    assert array_equal(processed_traces, output_case)

def test_get_max_efficiency():
    input_case = DataFrame({
        0: [1, 2, 8, 10],
        1: [1, 5, 6, 10]
    })
    output_case = Series([3, 4])
    max_efficiency = get_max_efficiency(input_case)
    assert array_equal(max_efficiency, output_case)

def ct2vl_alternate_derivation(ct, intercept, slope, ctl, vl):
    intercept = slope + (intercept + 1) 
    log_v = log(vl) + (ctl - 1 + intercept / slope) * log(slope * (ctl - 1) + intercept) - (ct - 1 + intercept / slope) * log(slope * (ct - 1) + intercept)  + ct - ctl
    return exp(log_v)

def test_ct_value_to_viral_load():
    ct_value_to_viral_load_input = [20.0, 1.0, -0.006, 37.96, 100.0]
    alternate_viral_load = ct2vl_alternate_derivation(*ct_value_to_viral_load_input)
    viral_load = ct_value_to_viral_load(*ct_value_to_viral_load_input)
    assert isclose(alternate_viral_load, viral_load)
    
