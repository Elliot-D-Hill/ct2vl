from dataclasses import dataclass, field
from typing import Union
from numpy import array, empty, exp, log, ndarray, atleast_1d
from pandas import DataFrame, read_csv
from scipy.integrate import quad
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures


@dataclass
class Converter:
    traces: Union[str, DataFrame, ndarray]
    LoD: ndarray
    Ct_at_LoD: ndarray
    max_replication_rate_cycle: array = field(init=False)
    max_replication_rate: array = field(init=False)
    model: LinearRegression = field(init=False)

    def __post_init__(self):
        self.get_traces(self.traces)
        self.preprocess_traces()
        self.get_max_replication_rate()
        self.calibrate()

    def get_traces(self, traces):
        options = {str: read_csv, DataFrame: lambda df: df, ndarray: DataFrame}
        self.traces = options[type(traces)](traces)

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

    def get_max_replication_rate(self):
        # Divide i+1th value by the ith value
        replication_rate = self.traces.div(self.traces.shift().bfill())
        self.max_replication_rate_cycle = (
            replication_rate.idxmax().astype(int).to_numpy().reshape(-1, 1)
        )
        self.max_replication_rate = replication_rate.max().to_numpy().reshape(-1, 1)

    def calibrate(self):
        pipeline = make_pipeline(
            PolynomialFeatures(), LinearRegression(fit_intercept=False)
        )
        cv = GridSearchCV(pipeline, {"polynomialfeatures__degree": [1, 2, 3]})
        cv.fit(X=self.max_replication_rate_cycle, y=self.max_replication_rate)
        self.model = cv.best_estimator_

    def log_replication_rate(self, Ct):
        return log(self.model.predict(array([[Ct]])))

    def ct_to_viral_load(self, Ct):
        Ct = atleast_1d(Ct)
        viral_loads = empty(Ct.shape)
        for i, ct_i in enumerate(Ct):
            integral_Ct, _ = quad(self.log_replication_rate, 0, ct_i)
            integral_Ct_at_LoD, _ = quad(self.log_replication_rate, 0, self.Ct_at_LoD)
            viral_loads[i] = exp(log(self.LoD) + integral_Ct_at_LoD - integral_Ct)
        return viral_loads
