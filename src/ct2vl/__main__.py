from ct2vl.cli import configure_arguments
from ct2vl.ct2vl import CT2VL, format_results
from pandas import read_csv
from pathlib import Path

def main():
    calibration_path = Path('ct2vl_calibration.pkl')
    parser = configure_arguments()
    args = parser.parse_args()
    if args.mode == 'calibrate':
        traces = read_csv(args.infile)
        converter = CT2VL(args.LoD, args.Ct_at_LoD, traces)
        converter.save(calibration_path)
    elif args.mode == 'convert':
        if not calibration_path.is_file():
            raise ValueError("You must calibrate ct2vl before you can use the convert argument")
        calibrated_converted = CT2VL.load(calibration_path)
        viral_load = calibrated_converted.ct_to_viral_load(args.Ct)
        formatted_results = format_results(args.Ct, viral_load)
        print(formatted_results)
        if args.outfile:
            formatted_results.to_csv(args.outfile, sep='\t', float_format='%.3f', index=False)

if __name__ == '__main__':
    main()