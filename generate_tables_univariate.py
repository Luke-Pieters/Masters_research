import pandas as pd
from tabulate import tabulate
from os import makedirs

#UNIVARIATE CASES
schemes = ["EWMA","HWMA","MEWMA","MHWMA","EEWMA","EHWMA"]
results_dict = {}
for s in schemes:
    results_dict[s] = pd.read_csv(f"results/univariate_results/{s}_ARL_SDRL_MRL_results.csv")

filepath = "./results/univariate_results/tables"
makedirs(filepath, exist_ok=True)

for s in schemes:
    df = pd.pivot_table(results_dict[s],values='ARL', index='Delta',columns='Parameter_string')
    print(s)
    print(df)
    print('='*30)
    
    parms = list(pd.unique(results_dict[s]['Parameter_string']))

    if 'phi2' in parms[0]:
        parms = [ x.replace('phi=','$\phi_1$=') for x in parms]
        parms = [ x.replace('phi2','$\phi_2$') for x in parms]
        parms = [ x.replace(',',' ') for x in parms]
    else:
        parms = [ x.replace('phi','$\phi$') for x in parms]
        parms = [ x.replace(',',' ') for x in parms]

    parms = ['$\delta$'] + parms
    print(parms)

    tbl = tabulate(df,parms,tablefmt="latex_raw",floatfmt=".1f",showindex="always")
    filename = filepath + "/" + s + "_table.txt"
    with open(filename, "w") as f:
      print(tbl, file=f)
