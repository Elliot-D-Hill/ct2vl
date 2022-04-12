from ct2vl.cli import configure_arguments
from ct2vl.ct2vl import CT2VL
from pandas import read_csv
from pathlib import Path

def main():
    calibration_path = Path('ct2vl_calibration.pkl')
    parser = configure_arguments()
    args = parser.parse_args()
    if args.mode == 'calibrate':
        traces = read_csv(args.infile)
        converter = CT2VL(traces, args.LoD, args.Ct_at_LoD)
        converter.save(calibration_path)
    elif args.mode == 'convert':
        if not calibration_path.is_file():
            raise ValueError("You must calibrate ct2vl before you can use the convert argument")
        calibrated_converted = CT2VL.load(calibration_path)
        results = calibrated_converted.convert(args.Ct)
        print(results)
        if args.outfile:
            results.to_csv(args.outfile, sep='\t', float_format='%.3f', index=False)

if __name__ == '__main__':
    main()