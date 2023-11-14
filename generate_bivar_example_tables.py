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
sig_0 = sig_0/5

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

cols = ['t','X11','X12','X13','X14','X15','X21','X22','X23','X24','X25','T2','OOC']
col_symb = ['t','X11','X12','$X_1$','X14','X15','X21','X22','$X_2$','X24','X25']
col_symb = ["{\color[HTML]{FFFFFF}" + x + "}" for x in col_symb]
col_symb += ["{\color[HTML]{FFFFFF} $T^2$ }"]
col_symb += ["{\color[HTML]{FFFFFF} OOC }"]

spacing = "{ | " + ">{\\\\centering\\\\arraybackslash}m{0.02\\\\textwidth} | " 
spacing += ">{\\\\centering\\\\arraybackslash}m{0.045\\\\textwidth} "*(5) + "|"
spacing += ">{\\\\centering\\\\arraybackslash}m{0.045\\\\textwidth} "*(5) + "|"
spacing += ">{\\\\centering\\\\arraybackslash}m{0.04\\\\textwidth} " + "|"
spacing += ">{\\\\centering\\\\arraybackslash}m{0.045\\\\textwidth}"
spacing += " | }"

float_fmt = ['.2f']*(len(cols)-1)
float_fmt = ['.0f'] + float_fmt
float_fmt = tuple(float_fmt)

tbl = str(tabulate(mod_tbl,col_symb,tablefmt="latex_raw",floatfmt=float_fmt,showindex="never"))
tbl = re.sub(r"\{r+l\}",spacing,tbl)
tbl = re.sub(r"X\d{2}","",tbl)
tbl = re.sub(r"True",r"{\\color[HTML]{B2182B}True}",tbl)
tbl = re.sub(r"\\hline",r"\\hline \\rowcolor[HTML]{4A6FCC} ",tbl,count=1)
print(tbl)

filename = filepath + "/" + "bivar_example_mod_chart_table.txt"
with open(filename, "w") as f:
    print(tbl, file=f)
    
tbl = str(tabulate(ex_tbl,col_symb,tablefmt="latex_raw",floatfmt=float_fmt,showindex="never"))
tbl = re.sub(r"\{r+l\}",spacing,tbl)
tbl = re.sub(r"X\d{2}","",tbl)
tbl = re.sub(r"True",r"{\\color[HTML]{B2182B}True}",tbl)
tbl = re.sub(r"\\hline",r"\\hline \\rowcolor[HTML]{4A6FCC} ",tbl,count=1)
print(tbl)

filename = filepath + "/" + "bivar_example_ex_chart_table.txt"
with open(filename, "w") as f:
    print(tbl, file=f)

