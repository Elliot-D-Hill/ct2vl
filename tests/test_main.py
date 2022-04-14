import sys
from pickle import load
from numpy import allclose, array
from pandas import read_csv
from pytest import raises
from tests import cases
from tests.utils import make_dummy_converter
from ct2vl.__main__ import main
from tests.test_ct2vl import LOD, CT_AT_LOD

def test_main_calibrate(tmp_path, monkeypatch):
    sys.argv[1:] = cases.configure_arguments_calibrate_input
    infile_path = str(tmp_path / 'test.csv')
    sys.argv[-1] = infile_path
    cases.calibrate_input.to_csv(infile_path, index=False)
    calibration_filepath = tmp_path/'calibration.pkl'
    with monkeypatch.context() as patched_context:
        patched_context.setattr('ct2vl.__main__.__file__', f'{tmp_path}/__main__.py')
        main()
        with open(calibration_filepath, 'rb') as f:
            converter = load(f)
    test_converter = make_dummy_converter(LOD, CT_AT_LOD, cases.calibrate_output[0], cases.calibrate_output[1])
    assert allclose(test_converter.intercepts, converter.intercepts)
    assert allclose(test_converter.slopes, converter.slopes)

def test_main_convert_uncalibrated(tmp_path, monkeypatch):
    sys.argv[1:] = cases.configure_arguments_convert_input
    with monkeypatch.context() as patched_context:
        patched_context.setattr('ct2vl.__main__.__file__', f'{tmp_path}/__main__.py')
        with raises(Exception):
            main()

def test_main_convert(tmp_path, monkeypatch):
    sys.argv[1:] = cases.configure_arguments_convert_input
    sys.argv[-1] = str(tmp_path / sys.argv[-1])
    calibration_filepath = tmp_path / 'calibration.pkl'
    intercepts = array([1, 1, 1])
    slopes = array([-0.001, -0.001, -0.001])
    converter = make_dummy_converter(LOD, CT_AT_LOD, intercepts, slopes)
    converter.save(calibration_filepath)
    with monkeypatch.context() as patched_context:
        patched_context.setattr('ct2vl.__main__.__file__', f'{tmp_path}/__main__.py')
        main()
    assert allclose(read_csv(sys.argv[-1], sep='\t'), cases.main_convert_output)
