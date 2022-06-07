from argparse import ArgumentParser
from re import A
import sys


def configure_arguments():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(
        dest="mode", help="modes include: calibrate or convert"
    )
    parser_calibrate = subparsers.add_parser("calibrate", help="Calibrates ct2vl")
    parser_calibrate.add_argument(
        "traces",
        type=str,
        help=("Filepath to a csv file containing PCR reaction traces"),
    )
    parser_calibrate.add_argument(
        "-s",
        "--calibration_series",
        type=str,
        help=(
            "A csv file containing the limit of detection (LoD): copies of SARS-CoV-2 viral genomes/mL"
            "(copies/mL; viral load at the LoD) and Ct value at the limit of detection (LoD)"
        ),
    )
    parser_calibrate.add_argument(
        "-l",
        "--LoD",
        type=float,
        required="--Ct_at_LoD" not in sys.argv,
        help=(
            "Limit of detection (LoD): copies of SARS-CoV-2 viral genomes/mL (copies/mL; viral load at the LoD)"
        ),
    )
    parser_calibrate.add_argument(
        "-c",
        "--Ct_at_LoD",
        type=float,
        required="--LoD" not in sys.argv,
        help=("Ct value at the limit of detection (LoD)"),
    )
    parser_convert = subparsers.add_parser(
        "convert", help="Predicts viral load from given Ct values"
    )
    parser_convert.add_argument(
        "Ct", nargs="+", type=float, help="Ct value to convert to viral load"
    )
    parser_convert.add_argument(
        "-o", "--outfile", type=str, help="Filepath for results"
    )
    return parser.parse_args()
