from pickle import dump, load
from numpy import column_stack, log10
from pandas import DataFrame
from ct2vl.cli import configure_arguments
from ct2vl.ct2vl import CT2VL
from pathlib import Path
from os.path import abspath, dirname

def main():
    module_path = Path(abspath(dirname(__file__)))
    filename = Path('calibration.pkl')
    calibration_filepath = module_path / filename
    args = configure_arguments()
    if args.mode == 'calibrate':
        converter = CT2VL(args.infile)
        with open(calibration_filepath, 'wb') as f:
            dump(converter, f)
        print('Calibration complete.')
    elif args.mode == 'convert':
        if not calibration_filepath.is_file():
            raise ValueError("You must calibrate ct2vl before you can use the convert argument")
        with open(calibration_filepath, 'rb') as f:
            calibrated_converter = load(f)
        print(args)
        viral_load = calibrated_converter.ct_to_viral_load(args.Ct, args.LoD, args.Ct_at_LoD)
        log10_viral_load = log10(viral_load)
        results = column_stack([args.Ct, viral_load, log10_viral_load])
        columns=['ct_value', 'viral_load', 'log10_viral_load']
        formatted_results = DataFrame(results, columns=columns)
        print(formatted_results)
        if args.outfile:
            formatted_results.to_csv(args.outfile, sep='\t', float_format='%.3f', index=False) 

if __name__ == '__main__':
    main() # pragma: no cover