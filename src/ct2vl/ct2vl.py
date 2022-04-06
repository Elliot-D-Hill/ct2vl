from numpy import exp, log


def preprocess_traces(traces):
    traces = traces.T
    # Remove first 3 rows, since early values tend to be noise
    traces = traces.iloc[3:]
    # Negative values are noise, so we can set them to zero.
    traces[traces < 0] = 0
    # Theoretically, product should only increase, so we can make the data monotonic.
    traces = traces.cummax()
    # Add a positive constant to prevent division by zero
    traces = traces + 1
    return traces

def get_max_efficiency(traces):
    # Divide i+1th value by the ith value
    ratio = (traces
        .div(traces
            .shift()
            .bfill()
        )
    )
    efficiency = ratio - 1
    return efficiency.max()

def ct_value_to_viral_load(ct, intercept, slope, ctl, vl):
    intercept = slope + (intercept + 1)
    ctl_efficiency = (slope * (ctl - 1)) + intercept
    ct_efficiency = (slope * (ct - 1)) + intercept
    efficiency_difference = (ctl_efficiency * log(ctl_efficiency)) - (ct_efficiency * log(ct_efficiency))
    log_v = log(vl) + (efficiency_difference / slope) + ct - ctl
    return exp(log_v)


