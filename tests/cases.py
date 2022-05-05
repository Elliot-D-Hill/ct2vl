from argparse import Namespace
from numpy import arange, array, diag, fill_diagonal, tile
from pandas import DataFrame

preprocess_traces_input = DataFrame({
        0: [1, 1, 0],
        1: [2, 2, 0],
        2: [3, 3, 0],
        3: [-1, 1, 0],
        4: [2, -2, 0],
        5: [1, 1, 1],
        6: [3, 2, 1]
})
preprocess_traces_output = DataFrame({
    0: [1, 3, 3, 4],
    1: [2, 2, 2, 3],
    2: [1, 1, 2, 2]
})

get_max_replication_rate_input = DataFrame({
    0: [1, 2, 8, 10],
    1: [1, 5, 6, 10]
})
get_max_replication_rate_output = (array([[2], [1]]), array([[4], [5]]))

calibrate_input = (
    array([[1.], [1.], [1.], [1.], [1.78571429], [1.61538462], [1.41666667], [1.18181818], [1.], [1.]]),
    array([[3], [3], [3], [3], [4], [5], [6], [7], [3], [3]])
)
calibrate_output = array([[0.80112388, 0.09970862]])

a = tile(arange(10, 0, -1), (10, 1))
fill_diagonal(a, diag(a)*2)
main_calibrate_input = DataFrame(a + a.T)
main_calibrate_output = calibrate_output

ct_to_viral_load_input = [37.83]
ct_to_viral_load_output = array([100.0])

configure_arguments_calibrate_input = ['calibrate', 'test.tsv']
configure_arguments_calibrate_output = Namespace(
    mode='calibrate', 
    infile='test.tsv'
)

configure_arguments_convert_input = ['convert', '100.0', '37.83', '37.83', '--outfile', 'test.tsv']
configure_arguments_convert_output = Namespace(
    mode='convert', 
    Ct=[37.83], 
    LoD=100.0,
    Ct_at_LoD=37.83,
    outfile='test.tsv'
)

main_convert_output = DataFrame({
    'ct_value': [37.83],
    'viral_load': [100.0],
    'log10_viral_load': [2],
 })