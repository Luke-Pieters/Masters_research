import spm_multivariate_sim_module as sim
import Multivariate_Schemes_module as spm_schemes
import json
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
import pandas as pd
import scipy.stats as sts
from ProgressBar_module import printProgressBar

#CHART TO TEST
n = 2

x_p = 2
x_names = [f"X{i+1}" for i in range(x_p)]
x_values = np.arange(-4,4.5,0.5)

true_parms = [3.0,2.0,5.0]
true_var = 1.0

print(x_values,np.mean(x_values))

X_df = pd.DataFrame()
for i in range(x_p):
    X_df[x_names[i]] = x_values**(i+1)

print(X_df)

sample_list = true_parms + [true_var]
sample_list = [np.array(sample_list)]

print(sample_list)

opt_k = lambda x: -x/2
phi = 0.25
chart = spm_schemes.MHWMA(p=(x_p+2),phi=phi,k=opt_k(phi),mean_0=sample_list[0],sig2_0=np.identity(x_p+2))
chart_name = chart.__class__.__name__
print("Chart: " + chart_name)

with open(f'results\multivar_{chart_name}_optimal_L.json') as json_file:
       L_arr = json.load(json_file)

L = L_arr[str(f"p={x_p+2}")][str(phi)]
chart.change_L(L)

# sts.norm(loc=mu_0,scale=sig_0).rvs(1)
# printProgressBar(iteration=0,total=n,prefix='Simulation Progress')
t_arr = []
for i in range(n):
    # printProgressBar(iteration=i,total=n,prefix='Simulation Progress')
    t = 0
    ooc = False
    while ooc == False and t < 2:
        t += 1
        Y = true_parms[0]
        for d in range(x_p):
            Y += true_parms[d+1]*X_df[x_names[d]] 
        Y += sts.norm(loc=0,scale=true_var).rvs(len(x_values))
        
        # print(Y)
        mdl = linear_model.LinearRegression()
        mdl.fit(X_df,Y)
        y_hat = mdl.predict(X_df)
        mse = mean_squared_error(Y,y_hat)

        est_parms = [mdl.intercept_]
        for d in range(x_p):
            est_parms += [mdl.coef_[d]]
        est_parms += [mse]
        sample_list += [np.array(est_parms)]
        St = chart.chart_stat(sample_list)
        T2 = chart.T2_stat(St,t)
        ooc = chart.check_ooc(St,t=t)

        print(f"t={t}",f"sample={est_parms}",f"St={St}",f"T2={T2}",f"L={chart.L}",f"ooc={ooc}")

    t_arr += [t]

    chart.reset_chart()

# printProgressBar(iteration=n,total=n,prefix='Simulation Progress')

print(t_arr)
print(np.mean(t_arr))