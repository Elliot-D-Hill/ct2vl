from ct2vl.cli import configure_arguments
from tests import cases

def test_configure_arguments_calibrate():
    args = configure_arguments(cases.configure_arguments_calibrate_input)    
    assert args == cases.configure_arguments_calibrate_output

def test_configure_arguments_convert():
    args = configure_arguments(cases.configure_arguments_convert_input)
    assert args == cases.configure_arguments_convert_output