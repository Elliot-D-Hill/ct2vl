from pickle import dump, load
from numpy import log10
from pandas import DataFrame, read_csv
from ct2vl.cli import configure_arguments
from ct2vl.ct2vl import CT2VL
from pathlib import Path
from os.path import abspath, dirname


def main():
    module_path = Path(abspath(dirname(__file__)))
    filename = Path("calibration.pkl")
    calibration_filepath = module_path / filename
    args = configure_arguments()

    if args.mode == "calibrate":
        if args.calibration_series is not None:
            df = read_csv(args.calibration_series)
            LoD = df.iloc[:, 0]
            Ct_at_LoD = df.iloc[:, 1]
        else:
            LoD = args.LoD
            Ct_at_LoD = args.Ct_at_LoD
        converter = CT2VL(args.traces, LoD, Ct_at_LoD)
        with open(calibration_filepath, "wb") as f:
            dump(converter, f)
        print("Calibration complete.")
    elif args.mode == "convert":
        if not calibration_filepath.is_file():
            raise ValueError(
                "You must calibrate ct2vl before you can use the convert argument"
            )
        with open(calibration_filepath, "rb") as f:
            calibrated_converter = load(f)
        viral_load = calibrated_converter.ct_to_viral_load(args.Ct)
        log10_viral_load = log10(viral_load)
        formatted_results = DataFrame(
            {
                "Ct": args.Ct,
                "viral_load": viral_load,
                "log10_viral_load": log10_viral_load,
            }
        )
        print(formatted_results)
        if args.outfile:
            formatted_results.to_csv(
                args.outfile, sep="\t", float_format="%.3f", index=False
            )


if __name__ == "__main__":
    main()  # pragma: no cover
