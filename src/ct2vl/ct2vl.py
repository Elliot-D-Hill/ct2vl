from dataclasses import dataclass, field
from pickle import dump, load
from numpy import array, concatenate, exp, log, log10
from pandas import DataFrame, read_csv
from sklearn.linear_model import LinearRegression


@dataclass
class CT2VL:
    LoD: float
    Ct_at_LoD: float
    intercept: float = field(init=False)
    slope: float = field(init=False)

    def efficiency(self, Ct):
        return (self.slope * Ct) + self.intercept

    def fit_model(self, X, y):
        model = LinearRegression(fit_intercept=True)
        model.fit(X=X, y=y)
        self.intercept = model.intercept_
        self.slope = model.coef_[0]

    def calibrate(self, traces_filepath):
        traces = read_csv(traces_filepath)
        traces = traces.reset_index(drop=True)
        ct_values = traces.iloc[:, 0]
        traces = traces.iloc[:, 1:]
        processed_traces = preprocess_traces(traces)
        max_efficiency, cycle_at_max_efficency = get_max_efficiency(processed_traces)
        cycle_at_max_efficency = cycle_at_max_efficency.to_numpy().reshape(-1, 1)
        ct_values = ct_values.to_numpy().reshape(-1, 1)
        self.fit_model(ct_values, max_efficiency)

    def ct_to_viral_load(self, Ct):
        Ct = array(Ct).reshape(-1, 1)
        self.intercept          = self.intercept + 1
        Ct_L_efficiency         = (self.slope * self.Ct_at_LoD) + self.intercept
        Ct_efficiency           = (self.slope * Ct) + self.intercept
        efficiency_difference   = (Ct_L_efficiency * log(Ct_L_efficiency)) - (Ct_efficiency * log(Ct_efficiency))
        log_viral_load          = log(self.LoD) + (efficiency_difference / self.slope) + Ct - self.Ct_at_LoD
        return exp(log_viral_load)

    def convert(self, Ct):
        viral_loads = self.ct_to_viral_load(Ct)
        return format_results(Ct, viral_loads)

    def save(self, filepath):
        with open(filepath, 'wb') as f:
            dump(self, f)

    @classmethod
    def load(cls, filepath):
        with open(filepath, 'rb') as f:
            return load(f)


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
    return efficiency.max(), efficiency.idxmax()

def format_results(Ct, viral_load):
    Ct = array(Ct).reshape(-1, 1)
    # viral_load = viral_load.to_numpy().reshape(-1, 1)
    log10_viral_load = log10(viral_load)
    results = concatenate([Ct, viral_load, log10_viral_load], axis=1)
    columns=['ct_value', 'viral_load', 'log10_viral_load']
    return DataFrame(results, columns=columns)
 