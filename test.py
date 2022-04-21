
from ct2vl.ct2vl import CT2VL
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress, pearsonr

def predict_vs_observed(x, y, validation_data, ax):
    fontsize = 18
    sns.set(rc = {'figure.figsize':(8,8)})
    sns.set_theme(style="white")
    g = sns.scatterplot(
        data=validation_data, 
        x=x, 
        y=y, 
        hue='machine',
        palette='deep',
        zorder=10,
        ax=ax)
    g.set_xlabel('Predicted viral load (copies/mL)', fontsize=fontsize)
    g.set_ylabel('Observed viral load (copies/mL)', fontsize=fontsize)
    sns.despine()

    max_range = validation_data[[x, y]].max().max()
    min_range = validation_data[[x, y]].min().min()
    x = np.linspace(min_range, max_range, 10)
    sns.lineplot(x=x, y=x, color='black', ax=ax)
    plt.tight_layout()

def main():
    alinity_Ct_at_LoD = 37.96
    alinity_LoD = 100.0
    converter = CT2VL(LoD=alinity_LoD, Ct_at_LoD=alinity_Ct_at_LoD)
    converter.calibrate('Data/positive_traces_with_ct_values.csv')
    print(converter.intercept, converter.slope)
    validation_data = pd.read_csv('Data/validation_data.csv')
    predicted = converter.convert(validation_data['ct_value'])
    validation_data['log10_viral_load'] = np.log10(validation_data['viral_load'])
    validation_data['predicted_viral_load'] = predicted['viral_load']
    validation_data['predicted_log10_viral_load'] = predicted['log10_viral_load']
    _, _, r, _, _ = linregress(
    validation_data['predicted_log10_viral_load'], 
        validation_data['log10_viral_load']
    )
    r_squared = r ** 2
    correlation = pearsonr(validation_data['predicted_log10_viral_load'], validation_data['log10_viral_load'])
    print(f'r2: {r_squared}')
    print(f'correlation: {correlation}')

    validation_data['ratio'] = validation_data['log10_viral_load'] / validation_data['predicted_log10_viral_load']
    validation_data['error'] = np.abs(validation_data['log10_viral_load'] - validation_data['predicted_log10_viral_load'])
    mean_ratio = validation_data['ratio'].mean()
    mean_error = validation_data['error'].mean()
    std_error = validation_data['error'].std()

    print(f'Ratio of observed over predicted: {mean_ratio:.4f}')
    print(f'Mean absolute error: {mean_error:.4f} +/- {std_error:.4f} log10(copies/mL)')

    data = validation_data.melt(id_vars='ct_value', value_vars=['viral_load', 'predicted_viral_load'])
    sns.set(rc = {'figure.figsize':(16,6)})
    f, axes = plt.subplots(1, 3)
    x = 'ct_value'
    y = 'value'
    fontsize = 18
    sns.set_theme(style="white")
    g = sns.scatterplot(
        data=data, 
        x=x, 
        y=y, 
        hue='variable',
        palette='deep',
        zorder=10,
        ax=axes[0])
    g.set_xlabel('ct value', fontsize=fontsize)
    g.set_ylabel('Viral load (copies/mL)', fontsize=fontsize)
    sns.despine()

    predict_vs_observed('predicted_viral_load', 'viral_load', validation_data, ax=axes[1])
    predict_vs_observed('predicted_log10_viral_load', 'log10_viral_load', validation_data, ax=axes[2])
    plt.show()


if __name__ == '__main__':
    main()