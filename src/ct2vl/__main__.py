from pickle import dump, load
from numpy import log10
from pandas import DataFrame, read_csv
from ct2vl.cli import configure_arguments
from ct2vl.conversion import Converter
from pathlib import Path
from os.path import abspath, dirname


def main():
    module_path = Path(abspath(dirname(__file__)))
    filename = Path("calibration.pkl")
    calibration_filepath = module_path / filename
    args = configure_arguments()

    if args.mode == "calibrate":
        print("LoD", args.LoD, "Ct_at_LoD", args.Ct_at_LoD)
        converter = Converter(args.traces, args.LoD, args.Ct_at_LoD)
        print(converter.ct_to_viral_load(21.1))
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
                "LoD": calibrated_converter.LoD,
                "Ct_at_LoD": calibrated_converter.Ct_at_LoD,
                "Ct": args.Ct,
                "viral_load": viral_load,
                "log10_viral_load": log10_viral_load,
            }
        )
        formatted_results.index += 1
        print(formatted_results)
        if args.outfile:
            formatted_results.to_csv(
                args.outfile, sep="\t", float_format="%.3f", index=False
            )


if __name__ == "__main__":
    main()  # pragma: no cover
