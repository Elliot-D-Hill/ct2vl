from numpy import array, empty, atleast_1d, log, exp
from scipy.integrate import quad
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from ct2vl.rates import make_rates


class Converter:
    """Uses PCR reaction curves to calibrate a model which converts Ct values to viral loads

    Parameters
    ----------
    traces: str, pandas.DataFrame, numpy.ndarray, or dict
        More commonly, a table where each row corresponds to a PCR reaction curve and
        each column is a cycle in the reaction.
        (OR, if this contains columns named max_replication_rate and max_replication_rate_cycle,
        these columns are parallel arrays where for trace[j], the maximum replication rate was
        max_replication_rate[j] and that rate was observed at cycle max_replication_rate_cycle[j].
        In the unlikely case that this is the type of input data you have.)
    LoD: float
        Limit of detection (LoD): copies of SARS-CoV-2 viral genomes/mL (copies/mL; viral load at the LoD)
    Ct_at_LoD
        Ct value at the limit of detection (LoD)
    """

    """
    Member variables
    ----------------
    LoD: float
    Ct_at_LoD: float
    max_replication_rate_cycle: array = field(init=False)
    max_replication_rate: array = field(init=False)
    model: LinearRegression = field(init=False)
    """

    def __init__(self, traces, LoD, Ct_at_LoD):
        self.replication_rate_supplier = make_rates(traces)
        self.calibrate()
        self.LoD = LoD
        self.Ct_at_LoD = Ct_at_LoD

    def calibrate(self):
        """Fits a polynomial linear regression, where the degree of the polynomial is chosen via
        5-fold grid search cross-validation.
        """
        pipeline = make_pipeline(
            PolynomialFeatures(), LinearRegression(fit_intercept=False)
        )
        cv = GridSearchCV(pipeline, {"polynomialfeatures__degree": [1, 2, 3]})
        cv.fit(
            X=self.replication_rate_supplier.max_replication_rate_cycle,
            y=self.replication_rate_supplier.max_replication_rate,
        )
        self.model = cv.best_estimator_

    def log_replication_rate(self, Ct):
        """Predicts the log replication rate for a give Ct value using a model fit"""
        return log(self.model.predict(array([[Ct]])))

    def ct_to_viral_load(self, Ct):
        """Converts Ct values to viral loads
        Parameters
        ----------
        Ct: Iterable[float] or float
        """
        Ct = atleast_1d(Ct)
        viral_loads = empty(Ct.shape)
        for i, ct_i in enumerate(Ct):
            integral_Ct, _ = quad(self.log_replication_rate, 0, ct_i)
            integral_Ct_at_LoD, _ = quad(self.log_replication_rate, 0, self.Ct_at_LoD)
            viral_loads[i] = exp(log(self.LoD) + integral_Ct_at_LoD - integral_Ct)
        return viral_loads
