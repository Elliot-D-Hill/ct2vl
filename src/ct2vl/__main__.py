from ct2vl.cli import configure_arguments
from ct2vl.ct2vl import convert_ct2vl, calibrate
from pandas import read_csv, read_pickle
from pathlib import Path
import pickle

def main():
    # TODO add directory for calibration config if it doesn exist
    calibration_path = Path('ct2vl_calibration.pkl')
    parser = configure_arguments()
    args = parser.parse_args()
    if args.mode == 'calibrate':
        traces = read_csv(args.infile)
        fit = calibrate(traces)
        calibration_config = {
            'fit': fit,
            'Ct_L': args.Ct_at_LoD,
            'v_L': args.LoD
        }
        with open(calibration_path, 'wb') as handle:
            pickle.dump(calibration_config, handle, protocol=pickle.HIGHEST_PROTOCOL)
    elif args.mode == 'convert':
        if not calibration_path.is_file():
            Exception("You must calibrate ct2vl before you can use the convert argument")
        calibration_config = read_pickle(calibration_path)
        results = convert_ct2vl(
            args.Ct, 
            calibration_config['fit'], 
            calibration_config['Ct_L'], 
            calibration_config['v_L']
        )
        results.to_csv(args.outfile, sep='\t', index=False)



if __name__ == '__main__':
    main()