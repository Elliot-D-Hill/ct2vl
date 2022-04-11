from numpy import array, exp, log, log10
from pandas import DataFrame
from sklearn.linear_model import TheilSenRegressor


class Converter:
    def __init__(self, traces, lod, ct_at_lod):
        self.ct_values = traces.iloc[:, 0]
        self.traces = traces.iloc[:, 1:]
        self.lod = lod
        self.ct_at_lod = ct_at_lod
        self.slope = None
        self.intercept = None
        self.calibrate()

    def preprocess_traces(self):
        self.traces = self.traces.T
        # Remove first 3 rows, since early values tend to be noise
        self.traces = self.traces.iloc[3:]
        # Negative values are noise, so we can set them to zero.
        self.traces[self.traces < 0] = 0
        # Theoretically, product should only increase, so we can make the data monotonic.
        self.traces = self.traces.cummax()
        # Add a positive constant to prevent division by zero
        self.traces = self.traces + 1

    def get_max_efficiency(self):
        # Divide i+1th value by the ith value
        ratio = (self.traces
            .div(self.traces
                .shift()
                .bfill()
            )
        )
        efficiency = ratio - 1
        return efficiency.max()

    def calibrate(self):
        max_efficiency = self.get_max_efficiency()
        model = TheilSenRegressor(fit_intercept=True)
        model.fit(x=self.ct_values, y=max_efficiency)
        self.slope = model.coef_
        self.intercept = model.intercept_
    
    def ct_value_to_viral_load(self, Ct):
        Ct = array(Ct)
        self.intercept = self.slope + (self.intercept + 1)
        Ct_L_efficiency = (self.slope * (self.Ct_L - 1)) + self.intercept
        Ct_efficiency = (self.slope * (Ct - 1)) + self.intercept
        efficiency_difference = (Ct_L_efficiency * log(Ct_L_efficiency)) - (Ct_efficiency * log(Ct_efficiency))
        log_v = log(self.v_L) + (efficiency_difference / self.slope) + Ct - self.Ct_L
        return exp(log_v)

    def format_results(self, Ct, viral_load):
        return DataFrame({
            'Ct_value': Ct,
            'viral_load': viral_load,
            'log10_viral_load': log10(viral_load)
        })

 