from argparse import ArgumentParser

def configure_arguments():
    parser = ArgumentParser()
    parser.add_argument(
        'infile',
        type=str,
        help=("Filepath containing Ct values and PCR reaction traces"))
    parser.add_argument(
        'outfile',
        type=str,
        help=("Filepath for the viral load estimates"))
    parser.add_argument(
        'Ct_L',
        type=float,
        help=("Ct value at the limit of detection (LoD)"))
    parser.add_argument(
        'v_L',
        type=float,
        help=("Limit of detection (LoD): copies of SARS-CoV-2 viral genomes/mL (copies/mL; viral load at the LoD)"))
    return parser