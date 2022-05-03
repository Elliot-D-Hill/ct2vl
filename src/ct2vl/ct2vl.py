from dataclasses import dataclass, field
from numpy import array, exp, log
from pandas import DataFrame, read_csv
from scipy.integrate import quad
from sklearn.linear_model import LinearRegression


@dataclass
class CT2VL:
    filepath: str
    LoD: float
    Ct_at_LoD: float
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

    def ct_to_viral_load(self, Ct):
        Ct = array([Ct]).flatten()
        viral_loads = []
        for ct_i in Ct:
            integral_Ct, _ = quad(self.rho, 0, ct_i)
            integral_Ct_at_LoD, _ = quad(self.rho, 0, self.Ct_at_LoD)
            log_viral_load = log(self.LoD) + integral_Ct_at_LoD - integral_Ct
            viral_load = exp(log_viral_load)
            viral_loads.append(viral_load)
        return array(viral_loads)

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
 