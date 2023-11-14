import pandas as pd
import numpy as np
import json
from tabulate import tabulate
from os import makedirs
import re

import Multivariate_Schemes_module as spm

# Read the CSV file
df = pd.read_csv('results\pm\Bivar_example_data.csv')

# Create an empty DataFrame to store the results
mean_df = pd.DataFrame()

# Iterate over the range from the second column to the end of the columns, with a step of 5
for i in range(1, len(df.columns), 5):
    # Select the 5 columns and calculate the mean
    mean = df.iloc[:, i:i+5].mean(axis=1)
    # Add the mean to the result DataFrame
    mean_df[f'mean_{i//5+1}'] = mean

# Print the result DataFrame
mean_df['t'] = df['t']
mean_df = mean_df[['t','mean_1','mean_2']]
mean_df.columns = ['t', 'X1', 'X2']
print(mean_df)

# Process parameters:
mean_0 = np.array([28.29, 45.85])
sig_0 = np.array([[0.0035, -0.0046], [-0.0046, 0.0226]])

opt_k = lambda x: -x/2

phi = 0.25
phi2=0.05
k = opt_k(phi)

mod_chart = spm.MHWMA(p=2,phi=phi,k=k,mean_0=mean_0,sig2_0=sig_0,L=9.88059)
ex_chart = spm.EHWMA(p=2,phi=phi,phi2=phi2,mean_0=mean_0,sig2_0=sig_0,L=10.296875)

mod_t2 = []
mod_ooc = []
ex_t2 = []
ex_ooc = []

series = [mean_0]

for r in range(mean_df.shape[0]):
    row = mean_df.iloc[r,1:]
    series += [np.array(row)]

    mod_stat = mod_chart.chart_stat(series=series)
    ex_stat = ex_chart.chart_stat(series=series)

    mod_t2 += [mod_chart.T2_stat(mod_stat,t=(r+1))]
    ex_t2 += [ex_chart.T2_stat(ex_stat,t=(r+1))]

    mod_ooc += [mod_chart.check_ooc(mod_stat,t=(r+1))]
    ex_ooc += [ex_chart.check_ooc(ex_stat,t=(r+1))]

mod_tbl = df.copy()
mod_tbl['T2'] = mod_t2
mod_tbl['OOC'] = mod_ooc

ex_tbl = df.copy()
ex_tbl['T2'] = ex_t2
ex_tbl['OOC'] = ex_ooc

filepath = "./results/examples"
makedirs(filepath, exist_ok=True)

mod_tbl.to_csv('./results/examples/MHWMA_bivar_exmpl_results.csv',index=False,mode='w')
ex_tbl.to_csv('./results/examples/EHWMA_bivar_exmpl_results.csv',index=False,mode='w')

