from argparse import ArgumentParser

def configure_arguments():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='subcommand', help='sub-commands include: fit, predict, and fit-predict')

    parser_calibrate = subparsers.add_parser('calibrate', help='Calibrates ct2vl')
    parser_calibrate.add_argument(
        'Ct_L',
        type=float,
        help=("Ct value at the limit of detection (LoD)"))
    parser_calibrate.add_argument(
        'v_L',
        type=float,
        help=("Limit of detection (LoD): copies of SARS-CoV-2 viral genomes/mL (copies/mL; viral load at the LoD)"))
    parser_calibrate.add_argument(
        'infile',
        type=str,
        help=("Filepath containing Ct values and PCR reaction traces"))
    parser_convert = subparsers.add_parser('convert', help='Predicts viral load from given Ct values')
    parser_convert.add_argument(
        'Ct', 
        nargs='+',
        type=float,
        help='Ct value to convert to viral load')
    parser_convert.add_argument(
        '-o',
        '--outfile',
        type=str,
        help='Filepath for results')
    return parser