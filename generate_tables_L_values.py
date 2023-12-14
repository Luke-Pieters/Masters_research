#save L values into tables
import pandas as pd
import json

from tabulate import tabulate
from os import makedirs
import re

# UNIVAR 
schemes = ["EWMA","HWMA","MEWMA","MHWMA","EEWMA","EHWMA"]
ex_schemes = ["EEWMA","EHWMA"]
mod_schemes = ["MEWMA","MHWMA"]

for s in schemes:
    L_df = pd.read_csv(f'results\L_tables\{s}_opt_L.csv')
    col_symb = L_df.columns
    
    col_symb = [ '$\\boldsymbol{' + x + '}$' for x in col_symb ]
    
    print(L_df)
    
    col_symb = ["{\color[HTML]{FFFFFF}" + x + "}" for x in col_symb]
    
    spacing = "{ | " + ">{\\\\centering\\\\arraybackslash}m{0.09\\\\textwidth} " 
    spacing += ">{\\\\centering\\\\arraybackslash}m{0.09\\\\textwidth} "*(len(L_df.columns)-1) 
    spacing += " | }"
    
    float_fmt = ['.3f']*(len(L_df.columns))
    float_fmt = tuple(float_fmt)
    
    tbl = str(tabulate(L_df,col_symb,tablefmt="latex_raw",floatfmt=float_fmt,showindex="never"))
    tbl = re.sub(r"\{r+\}",spacing,tbl)
    tbl = re.sub(r"nan",' ',tbl)
    tbl = re.sub(r" +",' ',tbl)
    tbl = re.sub(r"\\hline",r"\\hline \\rowcolor[HTML]{4A6FCC} ",tbl,count=1)
    # print(tbl)
    
    filepath = "./results/L_tables"
    makedirs(filepath, exist_ok=True)
    
    filename = filepath + "/" + f"{s}_opt_L_table.txt"
    with open(filename, "w") as f:
        print(tbl, file=f)

# # MULTIVAR

for s in schemes:
    L_df = pd.read_csv(f'results\L_tables\multivar_{s}_opt_L.csv')
    col_symb = L_df.columns
    
    col_symb = [ '$\\boldsymbol{' + x + '}$' for x in col_symb ]
    
    print(L_df)
    
    col_symb = ["{\color[HTML]{FFFFFF}" + x + "}" for x in col_symb]
        
    print(L_df)
    
    col_symb = ["{\color[HTML]{FFFFFF}" + x + "}" for x in col_symb]
    
    spacing = "{ | " + ">{\\\\centering\\\\arraybackslash}m{0.03\\\\textwidth} | " 
    spacing += ">{\\\\centering\\\\arraybackslash}m{0.09\\\\textwidth} "*(len(L_df.columns)-1) 
    spacing += " | }"
    
    float_fmt = ['.3f']*(len(L_df.columns)-1)
    float_fmt = ['.0f'] + float_fmt
    float_fmt = tuple(float_fmt)
    
    tbl = str(tabulate(L_df,col_symb,tablefmt="latex_raw",floatfmt=float_fmt,showindex="never"))
    tbl = re.sub(r"\{r+\}",spacing,tbl)
    tbl = re.sub(r"nan",' ',tbl)
    tbl = re.sub(r" +",' ',tbl)
    tbl = re.sub(r"\\hline",r"\\hline \\rowcolor[HTML]{4A6FCC} ",tbl,count=1)
    # print(tbl)
    
    filepath = "./results/L_tables"
    makedirs(filepath, exist_ok=True)
    
    filename = filepath + "/" + f"multivar_{s}_opt_L_table_p.txt"
    with open(filename, "w") as f:
        print(tbl, file=f)