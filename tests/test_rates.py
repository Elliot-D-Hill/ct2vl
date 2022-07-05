from numpy import allclose
from pytest import fixture
from ct2vl.rates import ReplicationRateFromTraces
from tests import cases


@fixture
def dummy_rate_calc(tmp_path):
    cases.main_calibrate_input.to_csv(f"{tmp_path}/infile", index=False)
    return ReplicationRateFromTraces(traces=f"{tmp_path}/infile")


# HERE
def test_preprocess_traces(dummy_rate_calc):
    dummy_rate_calc.traces = cases.preprocess_traces_input
    dummy_rate_calc.preprocess_traces()
    assert allclose(dummy_rate_calc.traces, cases.preprocess_traces_output)


def test_get_max_replication_rate(dummy_rate_calc):
    dummy_rate_calc.traces = cases.get_max_replication_rate_input
    dummy_rate_calc.get_max_replication_rate()
    assert allclose(
        dummy_rate_calc.max_replication_rate_cycle,
        cases.get_max_replication_rate_output[0],
    )
    assert allclose(
        dummy_rate_calc.max_replication_rate, cases.get_max_replication_rate_output[1]
    )
