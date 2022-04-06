from argparse import ArgumentParser

def configure_arguments():
    parser = ArgumentParser()
    parser.add_argument(
        'infile',
        type=str,
        help=("FIXME add a helpful message"))
    parser.add_argument(
        'outfile',
        type=str,
        help=("FIXME add a helpful message"))
    parser.add_argument(
        'ctl',
        type=float,
        help=("FIXME add a helpful message"))
    parser.add_argument(
        'vl',
        type=float,
        help=("FIXME add a helpful message"))
    return parser