import sys
from pickle import dump, load
from numpy import allclose
from pandas import read_csv
from pytest import raises
from tests import cases
from ct2vl.__main__ import main
from tests.test_conversion import dummy_converter


def test_main_calibrate(tmp_path, monkeypatch):
    sys.argv[1:] = cases.configure_arguments_calibrate_input
    infile_path = str(tmp_path / "test.csv")
    sys.argv[2] = infile_path
    cases.main_calibrate_input.to_csv(infile_path, index=False)
    calibration_filepath = tmp_path / "calibration.pkl"
    with monkeypatch.context() as patched_context:
        patched_context.setattr("ct2vl.__main__.__file__", f"{tmp_path}/__main__.py")
        main()
        with open(calibration_filepath, "rb") as f:
            converter = load(f)
    assert allclose(cases.calibrate_output, converter.model["linearregression"].coef_)


def test_main_convert_uncalibrated(tmp_path, monkeypatch):
    sys.argv[1:] = cases.configure_arguments_convert_input
    with monkeypatch.context() as patched_context:
        patched_context.setattr("ct2vl.__main__.__file__", f"{tmp_path}/__main__.py")
        with raises(Exception):
            main()


def test_main_convert(tmp_path, monkeypatch, dummy_converter):
    sys.argv[1:] = cases.configure_arguments_convert_input
    sys.argv[-1] = str(tmp_path / sys.argv[-1])
    calibration_filepath = tmp_path / "calibration.pkl"
    with open(calibration_filepath, "wb") as f:
        dump(dummy_converter, f)
    with monkeypatch.context() as patched_context:
        patched_context.setattr("ct2vl.__main__.__file__", f"{tmp_path}/__main__.py")
        main()
        print(read_csv(sys.argv[-1], sep="\t"))
        print(cases.main_convert_output)
    assert allclose(read_csv(sys.argv[-1], sep="\t"), cases.main_convert_output)
