from dataclasses import InitVar, dataclass, field
import pickle
from numpy import array, concatenate, exp, log, log10, median, ndarray
from pandas import DataFrame
from scipy.stats import theilslopes


@dataclass
class CT2VL:
    LoD: float
    Ct_at_LoD: float
    traces: InitVar[DataFrame] = None
    intercepts: float = field(init=False)
    slopes: float = field(init=False)

    def __post_init__(self, traces):
        if traces is None:
            return
        elif isinstance(traces, ndarray):
            traces = DataFrame(traces)
        elif not isinstance(traces, DataFrame):
            ValueError('traces must be a pandas dataframe or numpy ndarray')
        else:
            self.slopes, self.intercepts = calibrate(traces)
    
    def ct_to_viral_load(self, Ct):
        Ct = array(Ct).reshape(-1, 1)
        self.intercepts = self.slopes + (self.intercepts + 1)
        Ct_L_efficiency = (self.slopes * (self.Ct_at_LoD - 1)) + self.intercepts
        Ct_efficiency = (self.slopes * (Ct - 1)) + self.intercepts
        efficiency_difference = (Ct_L_efficiency * log(Ct_L_efficiency)) - (Ct_efficiency * log(Ct_efficiency))
        log_viral_load = log(self.LoD) + (efficiency_difference / self.slopes) + Ct - self.Ct_at_LoD
        return exp(log_viral_load)

    def save(self, filepath):
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, filepath):
        with open(filepath, 'rb') as f:
            return pickle.load(f)


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

def fit_model(ct_values, max_efficiency):
    slope, intercept, low_95ci_slope, high_95ci_slope = theilslopes(x=ct_values, y=max_efficiency)
    low_95ci_intercept = median(max_efficiency - (low_95ci_slope * ct_values))
    high_95ci_intercept = median(max_efficiency - (high_95ci_slope * ct_values))
    slopes = array([slope, low_95ci_slope, high_95ci_slope])
    intercepts = array([intercept, low_95ci_intercept, high_95ci_intercept])
    return slopes, intercepts

def calibrate(traces):
    ct_values = traces.iloc[:, 0]
    traces = traces.iloc[:, 1:]
    processed_traces = preprocess_traces(traces)
    max_efficiency = get_max_efficiency(processed_traces)
    return fit_model(ct_values, max_efficiency)

def format_results(Ct, viral_load):
    Ct = array(Ct).reshape(-1, 1)
    results = concatenate([Ct, viral_load, log10(viral_load)], axis=1)
    columns=['ct_value', 'viral_load', 'low_95ci', 'high_95ci', 'log10_viral_load', 'log10_low_95ci', 'log10_high_95ci']
    return DataFrame(results, columns=columns)

 