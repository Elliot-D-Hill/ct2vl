from argparse import Namespace
from numpy import array
from pandas import DataFrame, Series

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

get_max_efficiency_input = DataFrame({
    0: [1, 2, 8, 10],
    1: [1, 5, 6, 10]
})
get_max_efficiency_output = Series([3, 4])

fit_model_input = (
    array([1, 2, 3, 4, 5]),
    array([1, 2, 3, 4, 5])
)
fit_model_output = (
    array([1, 1, 1]),
    array([0, 0, 0])
)

calibrate_input = DataFrame({
    0: {0: 0.8750564234440642, 1: 0.9865798768034906, 2: 0.6341557195710585, 3: 0.5050754676772935, 4: 0.12440288838869917, 5: 0.34060694158291027},
    1: {0: 0.7584593082296942, 1: 0.34492464941537426, 2: 0.48094404923979883, 3: 0.7279021570663371, 4: 0.5517590715605767, 5: 0.20181061016891222}, 
    2: {0: 0.17615965059096927, 1: 0.07319539432862743, 2: 0.6080253776667448, 3: 0.6850836162752929, 4: 0.24491200257701817, 5: 0.5415637326389782},
    3: {0: 0.7230428547487858, 1: 0.7291131988748315, 2: 0.14549328978959353, 3: 0.25841170956286175, 4: 0.2447976425030478, 5: 0.7361196106532364},
    4: {0: 0.49863986044116837, 1: 0.07410915083853131, 2: 0.8235534622599857, 3: 0.9786167791619321, 4: 0.03864405742351951, 5: 0.9497405426423775},
    5: {0: 0.9043285564882163, 1: 0.6556362616487017, 2: 0.5302636778726645, 3: 0.1014387440138973, 4: 0.3446866928826079, 5: 0.9767517653587647}
})
calibrate_output = (
    array([-0.02074027,  0.44090545, -0.87505983]),
    array([ 0.28619202, -0.77404034,  1.53622872])
)

format_results_input = (
    array([[2], [3]]),
    array([[1, 1, 1], [1, 1, 1]])
)
format_results_output = DataFrame({
    'ct_value': {0: 2.0, 1: 3.0},
    'viral_load': {0: 1.0, 1: 1.0},
    'low_95ci': {0: 1.0, 1: 1.0},
    'high_95ci': {0: 1.0, 1: 1.0},
    'log10_viral_load': {0: 0.0, 1: 0.0},
    'log10_low_95ci': {0: 0.0, 1: 0.0},
    'log10_high_95ci': {0: 0.0, 1: 0.0}
 })

configure_arguments_calibrate_input = ['calibrate', '37.96', '100.0', 'test.csv']
configure_arguments_calibrate_output = Namespace(
    mode='calibrate', 
    LoD=37.96, 
    Ct_at_LoD=100.0, 
    infile='test.csv'
)

configure_arguments_convert_input = ['convert', '37.96', '--outfile', 'test.csv']
configure_arguments_convert_output = Namespace(
    mode='convert', 
    Ct=[37.96], 
    outfile='test.csv'
)

main_convert_output = DataFrame({
    'ct_value': [37.96],
    'viral_load': [100.0],
    'low_95ci': [100.0],
    'high_95ci': [100],
    'log10_viral_load': [2],
    'log10_low_95ci': [2],
    'log10_high_95ci': [2]
 })