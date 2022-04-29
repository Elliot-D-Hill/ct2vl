from dataclasses import dataclass, field
from pickle import dump, load

from numpy import array, concatenate, exp, log, log10
from pandas import DataFrame, read_csv
from scipy.integrate import quad
from sklearn.linear_model import LinearRegression


@dataclass
class CT2VL:
    filepath: str
    cycle_at_max_rho: array = field(init=False)
    max_rho: array = field(init=False)
    model: LinearRegression = field(init=False)

    def __post_init__(self):
        self.cycle_at_max_rho, self.max_rho = self.make_data()
        self.calibrate(self.cycle_at_max_rho, self.max_rho)
        
    def calibrate(self, X, y):
        self.model = LinearRegression().fit(X=X, y=y)

    def make_data(self):
        traces = read_csv(self.filepath)
        processed_traces = preprocess_traces(traces)
        cycle_at_max_rho, max_rho = get_max_rho(processed_traces)
        cycle_at_max_rho = cycle_at_max_rho.to_numpy().reshape(-1, 1)
        max_rho = max_rho.to_numpy().reshape(-1, 1)
        return cycle_at_max_rho, max_rho

    def rho(self, Ct):
        return log(self.model.predict(array([[Ct]])))

    def ct_to_viral_load(self, Ct, LoD, Ct_at_LoD):
        integral_Ct, _ = quad(self.rho, 0, Ct)
        integral_Ct_at_LoD, _ = quad(self.rho, 0, Ct_at_LoD)
        log_viral_load = log(LoD) + integral_Ct_at_LoD - integral_Ct
        return exp(log_viral_load)

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

def get_max_rho(traces):
    # Divide i+1th value by the ith value
    rho = (traces.div(traces.shift().bfill()))
    return rho.idxmax(), rho.max()

def format_results(Ct, viral_load):
    Ct = array(Ct).reshape(-1, 1)
    viral_load = viral_load.reshape(-1, 1)
    log10_viral_load = log10(viral_load)
    results = concatenate([Ct, viral_load, log10_viral_load], axis=1)
    columns=['ct_value', 'viral_load', 'log10_viral_load']
    return DataFrame(results, columns=columns)
 