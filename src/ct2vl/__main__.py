from pandas import read_csv,  DataFrame
from numpy import log10, median
from scipy.stats import theilslopes
from ct2vl.cli import configure_arguments
from ct2vl.ct2vl import preprocess_traces, get_max_efficiency, ct_value_to_viral_load


def main():
    parser = configure_arguments()
    args = parser.parse_args()
    traces = read_csv(args.infile)
    patient_ids = traces.pop('patient_id')
    ct_values = traces.pop('ct_value')
    processed_traces = preprocess_traces(traces)
    max_efficiency = get_max_efficiency(processed_traces)

    slope, intercept, upper_ci_slope, lower_ci_slope = theilslopes(x=ct_values, y=max_efficiency)
    lower_ci_intercept = median(max_efficiency - (lower_ci_slope * ct_values))
    upper_ci_intercept = median(max_efficiency - (upper_ci_slope * ct_values))

    viral_load = ct_value_to_viral_load(ct_values, intercept, slope, args.ctl, args.vl)
    lower_95_ci = ct_value_to_viral_load(ct_values, lower_ci_intercept, lower_ci_slope, args.ctl, args.vl)
    upper_95_ci = ct_value_to_viral_load(ct_values, upper_ci_intercept, upper_ci_slope, args.ctl, args.vl)

    results = DataFrame({
        'patient_id': patient_ids, 
        'ct_value': ct_values, 
        'viral_load': viral_load, 
        'lower_95_ci': lower_95_ci, 
        'upper_95_ci': upper_95_ci,
        'log10_viral_load': log10(viral_load),
        'log10_lower_95_ci': log10(lower_95_ci),
        'log10_upper_95_ci': log10(upper_95_ci)
    })

    results.to_csv(args.outfile, index=False)


if __name__ == '__main__':
    main()