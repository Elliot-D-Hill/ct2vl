from ct2vl.cli import configure_arguments
from ct2vl.ct2vl import CT2VL, format_results
from pathlib import Path
from os.path import abspath, dirname
from sys import argv

def main():
    module_path = Path(abspath(dirname(__file__)))
    filename = Path('calibration.pkl')
    calibration_filepath = module_path / filename
    args = configure_arguments(argv[1:])
    if args.mode == 'calibrate':
        converter = CT2VL(args.LoD, args.Ct_at_LoD)
        converter.calibrate(args.infile)
        converter.save(calibration_filepath)
        print('Calibration complete')
    elif args.mode == 'convert':
        if not calibration_filepath.is_file():
            raise ValueError("You must calibrate ct2vl before you can use the convert argument")
        calibrated_converted = CT2VL.load(calibration_filepath)
        viral_load = calibrated_converted.ct_to_viral_load(args.Ct)
        formatted_results = format_results(args.Ct, viral_load)
        print(formatted_results)
        if args.outfile:
            formatted_results.to_csv(args.outfile, sep='\t', float_format='%.3f', index=False) 

if __name__ == '__main__':
    main() # pragma: no cover