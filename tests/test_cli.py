from ct2vl.cli import configure_arguments
from tests import cases
import sys


def test_configure_arguments_calibrate():
    sys.argv[1:] = cases.configure_arguments_calibrate_input
    args = configure_arguments()
    assert args == cases.configure_arguments_calibrate_output


def test_configure_arguments_convert():
    sys.argv[1:] = cases.configure_arguments_convert_input
    args = configure_arguments()
    assert args == cases.configure_arguments_convert_output
