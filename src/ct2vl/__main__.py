from ct2vl.cli import configure_arguments
from ct2vl.ct2vl import convert_ct2vl


def main():
    parser = configure_arguments()
    args = parser.parse_args()
    results = convert_ct2vl(args.infile, args.Ct_L, args.v_L)
    results.to_csv(args.outfile, index=False)


if __name__ == '__main__':
    main()