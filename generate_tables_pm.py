import pandas as pd
from tabulate import tabulate
from os import makedirs
import re
import numpy as np

#UNIVARIATE CASES
schemes = ["MHWMA","EHWMA"]
values = ['ARL','SDRL','MRL']
results_dict = {}
parm_names = {0:"B0",
              1:"B1",
              2:"B2",
              3:"S2",
              '-':'-'}
for s in schemes:
    df = pd.read_csv(f"results/pm/{s}_pm_results.csv")
    results_dict[s] = df[df['Delta'] != 0]
    results_dict[s]['Parm'] = [parm_names[int(i)] for i in results_dict[s]['Parm']]
    

filepath = "./results/pm/tables"
makedirs(filepath, exist_ok=True)

for s in schemes:
    df = pd.pivot_table(results_dict[s],values=values, index=['Parm','Delta'])
    print(s)
    print(df)
    print('='*30) 
    measure_format = ['$\\boldsymbol{\ARL}$','$\\boldsymbol{\MRL}$','$\\boldsymbol{\SDRL}$']
    # parms = ['$\\boldsymbol{\delta}$'] + parms
    # parms = ["{\color[HTML]{FFFFFF}" + x + "}" for x in parms]
    measure_format = ["{\color[HTML]{FFFFFF}" + x + "}" for x in measure_format]
    measure_format = ['{\color[HTML]{FFFFFF}\\textbf{Parameter}} & {\color[HTML]{FFFFFF}$\\boldsymbol{\delta}$}'] + measure_format
    # print(parms)

    spacing = "{ | " + ">{\\\\centering\\\\arraybackslash}m{0.11\\\\textwidth} >{\\\\centering\\\\arraybackslash}m{0.03\\\\textwidth} | " + ">{\\\\centering\\\\arraybackslash}m{0.09\\\\textwidth} "*(3) + " | }"
    print(spacing)
    
    # float_fmt = ['.1f']*3
    # float_fmt = ['.2f'] + float_fmt
    # float_fmt = tuple(float_fmt)
    float_fmt = '.1f'

    tbl = str(tabulate(df,measure_format,tablefmt="latex_raw",floatfmt=float_fmt,showindex="always"))
    tbl = re.sub(r"\{lr+\}",spacing,tbl)
    tbl = re.sub(r"\\hline",r"\\hline \\rowcolor[HTML]{4A6FCC} ",tbl,count=1)
    for p in results_dict[s]['Parm']:
        parm_counter = 0
        for d in results_dict[s]['Delta']:
            parm_counter += 1
            if parm_counter == 2:
                tbl = re.sub(f"('{p}', {d})",f"${p}$ & {d}",tbl)
            else:
                tbl = re.sub(f"('{p}', {d})",f" & {d}",tbl)
    tbl = re.sub(r"B",r"\\beta_",tbl)
    tbl = re.sub(r"S2",r"\\sigma",tbl)
    tbl = re.sub(r"\(",r"",tbl)
    tbl = re.sub(r"\)",r"",tbl)
    
            
    
    # tbl = re.sub(r"\s+",' ',tbl)
    # tbl = re.sub("tabular","tabularx",tbl)
    filename = filepath + "/" + s + f"_pm_table.txt"
    with open(filename, "w") as f:
      print(tbl, file=f)

