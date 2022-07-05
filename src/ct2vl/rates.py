from abc import ABC, abstractmethod
from numpy import ndarray
from pandas import DataFrame, read_csv

class IReplicationRateSupplier(ABC):
    """ Abstract base class for classes that can supply the max_replication_rate
         and max_replication_rate_cycle arrays. """
    
    @abstractmethod
    def get_max_replication_rate(self):
        pass

    @abstractmethod
    def get_max_replication_rate_cycle(self):
        pass

class ReplicationRates(IReplicationRateSupplier):
    def get_max_replication_rate(self):
        raise Exception("Implement this")

    def get_max_replication_rate_cycle(self):
        raise Exception("Implement this")

class ReplicationRateFromTraces(IReplicationRateSupplier):
    def __init__(self, traces):
        self.get_traces(traces)
        self.preprocess_traces()
        self.calc_max_replication_rate()

    def get_traces(self, traces):
        """Converts input to pandas DataFrame

        Parameters
        ----------
        traces: str, pandas.DataFrame, or numpy.ndarray
            A table where each row corresponds to a PCR reaction curve and
            each column is a cycle in the reaction.
        """
        options = {str: read_csv, DataFrame: lambda df: df, ndarray: DataFrame}
        self.traces = options[type(traces)](traces)

    def preprocess_traces(self):
        """Preprocesses PRC reaction curves via dropping initial values,
        removing negative values, and making the values monotonic.
        """
        self.traces = self.traces.T
        # Remove first 3 rows, since early values tend to be noise
        self.traces = self.traces.iloc[3:]
        # Negative values are noise, so we can set them to zero.
        self.traces[self.traces < 0] = 0
        # Theoretically, product should only increase, so we can make the data monotonic.
        self.traces = self.traces.cummax()
        # Add a positive constant to prevent division by zero
        self.traces = self.traces + 1

    def calc_max_replication_rate(self):
        """Calculates the ratio between the (i+1)th and ith value of the reaction curve
        then takes the max and argmax of the sequence of ratios.
        """
        # Divide (i+1)th value by the ith value
        replication_rate = self.traces.div(self.traces.shift().bfill())
        self.max_replication_rate_cycle = (
            replication_rate.idxmax().astype(int).to_numpy().reshape(-1, 1)
        )
        self.max_replication_rate = replication_rate.max().to_numpy().reshape(-1, 1)

    def get_max_replication_rate(self):
        return self.max_replication_rate

    def get_max_replication_rate_cycle(self):
        return self.max_replication_rate_cycle
