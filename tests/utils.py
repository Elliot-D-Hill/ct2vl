from numpy import exp, log
from ct2vl.ct2vl import CT2VL

def make_dummy_converter(lod, ct_at_lod, intercept, slope):
    converter = CT2VL(lod, ct_at_lod)
    converter.intercepts = intercept
    converter.slopes = slope
    return converter

def ct2vl_alternate_derivation(ct, intercept, slope, ctl, vl):
    intercept = slope + (intercept + 1) 
    log_v = log(vl) + (ctl - 1 + intercept / slope) * log(slope * (ctl - 1) + intercept) - (ct - 1 + intercept / slope) * log(slope * (ct - 1) + intercept)  + ct - ctl
    return exp(log_v)