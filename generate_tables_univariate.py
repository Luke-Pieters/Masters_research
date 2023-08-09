import pandas as pd
from tabulate import tabulate
from os import makedirs
import re
import numpy as np

#UNIVARIATE CASES
schemes = ["EWMA","HWMA","MEWMA","MHWMA","EEWMA","EHWMA"]
values = 'ARL'
results_dict = {}
for s in schemes:
    df = pd.read_csv(f"results/univariate_results/{s}_ARL_SDRL_MRL_results.csv")
    results_dict[s] = df[df['Delta'] != 0]

filepath = "./results/univariate_results/tables"
makedirs(filepath, exist_ok=True)

for s in schemes:
    df = pd.pivot_table(results_dict[s],values=values, index='Delta',columns='Parameter_string')
    print(s)
    print(df)
    print('='*30)
    
    newcol = df.columns[1:]
    df_e = pd.DataFrame()
    measure = []
    for d1 in [0,1,2]:
        for d2 in [1,2,3]:
            if d2 < d1:
                continue
            
            temp_df = results_dict[s][(results_dict[s]['Delta']>d1)&(results_dict[s]['Delta']<=d2)]
            temp_df['Measure'] = f'E{values}({d1},{d2})'
            temp_df = pd.pivot_table(temp_df,values=values, index='Measure',columns='Parameter_string',aggfunc='mean')
            

            df_e = pd.concat([df_e,temp_df])   
            
    print(df_e)   
    
    parms = list(pd.unique(results_dict[s]['Parameter_string']))


    if 'k' in parms[0]:
        parms = [ x.split(',')[0]  for x in parms] #drop k

    if 'phi2' in parms[0]:
        parms = [ x.replace('phi=','$\\boldsymbol{\phi_1=') for x in parms]
        parms = [ x.replace('phi2','$\\boldsymbol{\phi_2') for x in parms]
        parms = [ x.replace(',','}$ ') for x in parms]
        parms = [ x + "}$" for x in parms]
    else:
        parms = [ x.replace('phi=','$\\boldsymbol{\phi_1=') for x in parms]
        parms = [ x + "}$" for x in parms]

    parms = ['$\\boldsymbol{\delta}$'] + parms
    parms = ["{\color[HTML]{FFFFFF}" + x + "}" for x in parms]
    print(parms)

    spacing = "{ | " + ">{\\\\centering\\\\arraybackslash}m{0.03\\\\textwidth} | " + ">{\\\\centering\\\\arraybackslash}m{0.09\\\\textwidth} "*(len(parms)-1) + " | }"
    print(spacing)

    tbl = str(tabulate(df,parms,tablefmt="latex_raw",floatfmt=".1f",showindex="always"))
    tbl = re.sub(r"\{r+\}",spacing,tbl)
    tbl = re.sub(r"\\hline",r"\\hline \\rowcolor[HTML]{4A6FCC} ",tbl,count=1)
    
    # tbl = re.sub(r"\s+",' ',tbl)
    # tbl = re.sub("tabular","tabularx",tbl)
    filename = filepath + "/" + s + f"_{values}_table.txt"
    with open(filename, "w") as f:
      print(tbl, file=f)
    
    parms[0] = ' '
    spacing = "{ | " + ">{\\\\centering\\\\arraybackslash}m{0.1\\\\textwidth} | " + ">{\\\\centering\\\\arraybackslash}m{0.09\\\\textwidth} "*(len(parms)-1) + " | }"
      
    tbl = str(tabulate(df_e,parms,tablefmt="latex_raw",floatfmt=".1f",showindex="always"))
    tbl = re.sub(r"\{lr+\}",spacing,tbl)
    tbl = re.sub(r"\\hline",r"\\hline \\rowcolor[HTML]{4A6FCC} ",tbl,count=1)
    
    filename = filepath + "/" + s + f"_E{values}_table.txt"
    with open(filename, "w") as f:
      print(tbl, file=f)
