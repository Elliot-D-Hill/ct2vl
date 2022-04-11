from numpy import array, exp, log, log10, median
from pandas import DataFrame
from scipy.stats import theilslopes


def preprocess_traces(traces):
    traces = traces.T
    # Remove first 3 rows, since early values tend to be noise
    traces = traces.iloc[3:]
    # Negative values are noise, so we can set them to zero.
    traces[traces < 0] = 0
    # Theoretically, product should only increase, so we can make the data monotonic.
    traces = traces.cummax()
    # Add a positive constant to prevent division by zero
    traces = traces + 1
    return traces


def get_max_efficiency(traces):
    # Divide i+1th value by the ith value
    ratio = (traces
        .div(traces
            .shift()
            .bfill()
        )
    )
    efficiency = ratio - 1
    return efficiency.max()


def get_intercept(slope, max_efficiency, ct_values):
    return median(max_efficiency - (slope * ct_values))


def fit_model(ct_values, max_efficiency):
    slope, intercept, upper_ci_slope, lower_ci_slope = theilslopes(x=ct_values, y=max_efficiency)
    lower_ci_intercept = get_intercept(lower_ci_slope, max_efficiency, ct_values)
    upper_ci_intercept = get_intercept(upper_ci_slope, max_efficiency, ct_values)
    intercepts = [intercept, lower_ci_intercept, upper_ci_intercept]
    slopes = [slope, lower_ci_slope, upper_ci_slope]
    return DataFrame({
        'type': ['estimate', 'lower_95_ci', 'upper_95_ci'],
        'intercept': intercepts, 
        'slope': slopes
    })


def ct_value_to_viral_load(Ct, intercept, slope, Ct_L, vl):
    Ct = array(Ct)
    intercept = slope + (intercept + 1)
    Ct_L_efficiency = (slope * (Ct_L - 1)) + intercept
    Ct_efficiency = (slope * (Ct - 1)) + intercept
    efficiency_difference = (Ct_L_efficiency * log(Ct_L_efficiency)) - (Ct_efficiency * log(Ct_efficiency))
    log_v = log(vl) + (efficiency_difference / slope) + Ct - Ct_L
    return exp(log_v)


def format_results(ct_values, viral_load):
    viral_load = DataFrame(viral_load, index=['viral_load', 'lower_95_ci', 'upper_95_ci']).T
    viral_load[['log10_viral_load', 'log10_lower_95_ci', 'log10_upper_95_ci']] = log10(viral_load)
    viral_load.insert(0, 'ct_value', ct_values)
    return viral_load


def calibrate(traces):
    ct_values = traces.iloc[:, 0]
    traces = traces.iloc[:, 1:]
    processed_traces = preprocess_traces(traces)
    max_efficiency = get_max_efficiency(processed_traces)
    return fit_model(ct_values, max_efficiency)
    

def convert_ct2vl(ct_values, fit, Ct_at_LoD, LoD):
    viral_load = [ct_value_to_viral_load(ct_values, intercept, slope, Ct_at_LoD, LoD) 
        for intercept, slope in zip(fit['intercept'], fit['slope'])]
    return format_results(ct_values, viral_load)
 