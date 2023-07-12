import spm_sim_module as sim
import Schemes_module as spm_schemes
import json
import numpy as np
from sklearn import linear_model
import pandas as pd
import scipy.stats as sts
from ProgressBar_module import printProgressBar

#CHART TO TEST
chart = spm_schemes.MHWMA()
chart_name = chart.__class__.__name__
print("Chart: " + chart_name)
n = 10

x_p = 2
x_names = [f"X{i+1}" for i in range(x_p)]
x_values = np.arange(-4,5,1)

true_parms = [3,2,5]
true_var = 1

print(x_values,np.mean(x_values))

X_df = pd.DataFrame()
for x in x_names:
    X_df[x] = x_values

print(X_df)

# sts.norm(loc=mu_0,scale=sig_0).rvs(1)
printProgressBar(iteration=0,total=n,prefix='Simulation Progress')
for i in range(n):
    printProgressBar(iteration=i,total=n,prefix='Simulation Progress')
    Y = true_parms[0] + true_parms[1]*X_df[x_names[0]] + true_parms[2]*X_df[x_names[1]] + sts.norm(loc=0,scale=true_var).rvs(len(x_values))

    mdl = 0

printProgressBar(iteration=n,total=n,prefix='Simulation Progress')