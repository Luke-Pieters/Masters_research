import spm_multivariate_sim_module as sim
import Multivariate_Schemes_module as spm_schemes
import json
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
import pandas as pd
import scipy.stats as sts
from ProgressBar_module import printProgressBar
from os import makedirs

#CHART TO TEST
n = 100

x_p = 2
x_names = [f"X{i+1}" for i in range(3)]
x_values = np.arange(-4,4.5,0.5)

true_parms = [3.0,2.0,5.0]
true_var = 1.0

change_parms = np.zeros(len(true_parms))
delta_arr = [0, 0.5, 1.5, 3.0]
# delta_arr = np.arange(0,3.25,0.25)

print(x_values,np.mean(x_values))

X_df = pd.DataFrame()
for i in range(3):
    X_df[x_names[i]] = x_values**(i)

print(X_df)

X_X = np.linalg.inv(np.array(X_df).T@np.array(X_df))

True_sig = np.zeros((4,4))

for i in range(3):
    for j in range(3):
        True_sig[i,j] = X_X[i,j]
        
True_sig[3,3] = 1

sample_list = true_parms + [true_var]
sample_list = [np.array(sample_list)]

print(sample_list)

opt_k = lambda x: -x/2
phi = 0.25
chart = spm_schemes.MHWMA(p=(x_p+2),phi=phi,k=opt_k(phi),mean_0=sample_list[0],sig2_0=True_sig)
chart_name = chart.__class__.__name__
print("Chart: " + chart_name)

with open(f'results\multivar_{chart_name}_optimal_L.json') as json_file:
       L_arr = json.load(json_file)

L = L_arr[str(f"p={x_p+2}")][str(phi)]
chart.change_L(L)

# sts.norm(loc=mu_0,scale=sig_0).rvs(1)
# 

#=======================================================================================================================
#=======================================================================================================================
#=======================================================================================================================
#=======================================================================================================================
#=======================================================================================================================
#=======================================================================================================================

filepath = "./results/pm/"
# filename = filepath + "/" + chart_name + "_ARL_SDRL_MRL_results.csv"
filename = filepath + "/" + chart_name + "_pm_results.csv"
ml_filename = filepath + "/" + chart_name + "_ml_data.csv"
makedirs(filepath, exist_ok=True)

parm_names = {0:"B0",
              1:"B1",
              2:"B2",
              3:"S2"}

output_df = pd.DataFrame(columns=['Parm','Delta','ARL','SDRL','MRL','Phi'])
ml_df = pd.DataFrame(columns=['Parm','Delta','B0','B1','B2','S2','T2'])
ic_count = 0
for p in range(len(true_parms)+1):
    print("_"*30)
    print(f"Parameter: {parm_names[p]}")
    print("_"*30)
    for d in delta_arr:
        if (d==0)&(ic_count >0):
            continue #only do d=0 once

        print("="*30)
        print(f"Delta: {d}")
        print("="*30)

        if d==0:
            ic_count += 1

        if p < len(true_parms):
            shift_vec = change_parms
            shift_vec[p] = d*np.sqrt(True_sig[p,p]) 
            sim_parm = true_parms + shift_vec
            sim_var = true_var
        else:
            sim_var = (1 + d)*2
            sim_parm = true_parms
        t_arr = []
        printProgressBar(iteration=0,total=n,prefix='Simulation Progress')
        for i in range(n):
            printProgressBar(iteration=i,total=n,prefix='Simulation Progress')
            t = 0
            ooc = False
            while ooc == False and t < 220:
                t += 1
                Y = 0
                for j in range(3):
                    Y += sim_parm[j]*X_df[x_names[j]] 
                Y += sts.norm(loc=0,scale=sim_var).rvs(len(x_values))
                
                # print(Y)
                mdl = linear_model.LinearRegression(fit_intercept=False)
                mdl.fit(X_df,Y)
                y_hat = mdl.predict(X_df)
                mse = mean_squared_error(Y,y_hat)

                est_parms = []
                for j in range(len(mdl.coef_)):
                    est_parms += [mdl.coef_[j]]
                est_parms += [mse]
                sample_list += [np.array(est_parms)]
                St = chart.chart_stat(sample_list)
                T2 = chart.T2_stat(St,t)
                ooc = chart.check_ooc(St,t=t)

                # print(f"t={t}",f"sample={est_parms}",f"St={St}",f"T2={T2}",f"L={chart.L}",f"ooc={ooc}")

            t_arr += [t]

            ml_newrow = pd.Series({'Parm': p,
                            'Delta': d,
                            'B0': sample_list[-1][0],
                            'B1': sample_list[-1][1],
                            'B2':sample_list[-1][2],
                            'S2':sample_list[-1][3],
                            'T2':T2})
            
            ml_df = pd.concat([ml_df,ml_newrow.to_frame().T],ignore_index=True)
            ml_df.to_csv(ml_filename,index=False,mode='w') #update csv file

            chart.reset_chart()

        ARL = np.mean(t_arr)
        SDRL = np.std(t_arr)
        MRL = np.median(t_arr)

        newrow = pd.Series({'Parm': p,
                            'Delta': d,
                            'ARL': ARL,
                            'SDRL': SDRL,
                            'MRL': MRL,
                            'Phi':phi})
        
        output_df = pd.concat([output_df,newrow.to_frame().T],ignore_index=True)
        output_df.to_csv(filename,index=False,mode='w') #update csv file 

        printProgressBar(iteration=n,total=n,prefix='Simulation Progress')
        
        
#OUTPUT
print(output_df)

print(ml_df.info())
# filename = filepath + "/" + chart_name + "_ARL_SDRL_MRL_results.csv"
# output_df.to_csv(filename,index=False)  

print("Output DataFrame saved to: " + filename)

#===============================================================================================================================
#===============================================================================================================================
#===============================================================================================================================
#===============================================================================================================================
#===============================================================================================================================
#===============================================================================================================================
#SHORT EXAMPLE DATA GENERATION 
n = 5 #number of IC samples 

sample_list = true_parms + [true_var]
sample_list = [np.array(sample_list)]
chart.reset_chart()

ml_exmpl_df = pd.DataFrame(columns=['t','Parm','Delta','B0','B1','B2','S2','T2','OOC'])

filepath = "./results/pm/"
# filename = filepath + "/" + chart_name + "_ARL_SDRL_MRL_results.csv"
filename = filepath + "/" + chart_name + "_pm_results.csv"
ml_exmpl_filename = filepath + "/" + chart_name + "_ml_exmpl_data.csv"
makedirs(filepath, exist_ok=True)
ooc = False

d=0
sim_parm = true_parms
sim_var = true_var
p=-1
for t in range(n):
                Y = sim_parm[0]
                for j in range(x_p):
                    Y += sim_parm[j+1]*X_df[x_names[j]] 
                Y += sts.norm(loc=0,scale=sim_var).rvs(len(x_values))
                
                # print(Y)
                mdl = linear_model.LinearRegression()
                mdl.fit(X_df,Y)
                y_hat = mdl.predict(X_df)
                mse = mean_squared_error(Y,y_hat)

                est_parms = [mdl.intercept_]
                for j in range(x_p):
                    est_parms += [mdl.coef_[j]]
                est_parms += [mse]
                sample_list += [np.array(est_parms)]
                St = chart.chart_stat(sample_list)
                T2 = chart.T2_stat(St,t)
                ooc = chart.check_ooc(St,t=t)

                # print(f"t={t}",f"sample={est_parms}",f"St={St}",f"T2={T2}",f"L={chart.L}",f"ooc={ooc}")

                ml_newrow = pd.Series({'t': t+1,
                                       'Parm': p,
                                        'Delta': d,
                                        'B0': sample_list[-1][0],
                                        'B1': sample_list[-1][1],
                                        'B2':sample_list[-1][2],
                                        'S2':sample_list[-1][3],
                                        'T2':T2,
                                        'OOC':ooc})
                
                ml_exmpl_df = pd.concat([ml_exmpl_df,ml_newrow.to_frame().T],ignore_index=True)
                ml_exmpl_df.to_csv(ml_exmpl_filename,index=False,mode='w') #update csv fil

#ADD SMALL SHIFT TO PARM 1
d=3
p=1
t+= 1
shift_vec = change_parms
shift_vec[p] = d*np.sqrt(true_var) 
sim_parm = true_parms + shift_vec
sim_var = true_var

Y = sim_parm[0]
for j in range(x_p):
    Y += sim_parm[j+1]*X_df[x_names[j]] 
Y += sts.norm(loc=0,scale=sim_var).rvs(len(x_values))

# print(Y)
mdl = linear_model.LinearRegression()
mdl.fit(X_df,Y)
y_hat = mdl.predict(X_df)
mse = mean_squared_error(Y,y_hat)

est_parms = [mdl.intercept_]
for j in range(x_p):
    est_parms += [mdl.coef_[j]]
est_parms += [mse]
sample_list += [np.array(est_parms)]
St = chart.chart_stat(sample_list)
T2 = chart.T2_stat(St,t)
ooc = chart.check_ooc(St,t=t)

ml_newrow = pd.Series({'t': t+1,
                        'Parm': p,
                        'Delta': d,
                        'B0': sample_list[-1][0],
                        'B1': sample_list[-1][1],
                        'B2':sample_list[-1][2],
                        'S2':sample_list[-1][3],
                        'T2':T2,
                        'OOC':ooc})

ml_exmpl_df = pd.concat([ml_exmpl_df,ml_newrow.to_frame().T],ignore_index=True)
ml_exmpl_df.to_csv(ml_exmpl_filename,index=False,mode='w') #update csv file

#ADD medium SHIFT TO PARM 2
d=2
p=2
t+= 1
shift_vec = change_parms
shift_vec[p] = d*np.sqrt(true_var) 
sim_parm = true_parms + shift_vec
sim_var = true_var

Y = sim_parm[0]
for j in range(x_p):
    Y += sim_parm[j+1]*X_df[x_names[j]] 
Y += sts.norm(loc=0,scale=sim_var).rvs(len(x_values))

# print(Y)
mdl = linear_model.LinearRegression()
mdl.fit(X_df,Y)
y_hat = mdl.predict(X_df)
mse = mean_squared_error(Y,y_hat)

est_parms = [mdl.intercept_]
for j in range(x_p):
    est_parms += [mdl.coef_[j]]
est_parms += [mse]
sample_list += [np.array(est_parms)]
St = chart.chart_stat(sample_list)
T2 = chart.T2_stat(St,t)
ooc = chart.check_ooc(St,t=t)

ml_newrow = pd.Series({'t': t+1,
                        'Parm': p,
                        'Delta': d,
                        'B0': sample_list[-1][0],
                        'B1': sample_list[-1][1],
                        'B2':sample_list[-1][2],
                        'S2':sample_list[-1][3],
                        'T2':T2,
                        'OOC':ooc})

ml_exmpl_df = pd.concat([ml_exmpl_df,ml_newrow.to_frame().T],ignore_index=True)
ml_exmpl_df.to_csv(ml_exmpl_filename,index=False,mode='w') #update csv file

#ADD large SHIFT TO VAR
d=1
p=3
t+= 1 
sim_parm = true_parms 
sim_var = (1 + d)*2

Y = sim_parm[0]
for j in range(x_p):
    Y += sim_parm[j+1]*X_df[x_names[j]] 
Y += sts.norm(loc=0,scale=sim_var).rvs(len(x_values))

# print(Y)
mdl = linear_model.LinearRegression()
mdl.fit(X_df,Y)
y_hat = mdl.predict(X_df)
mse = mean_squared_error(Y,y_hat)

est_parms = [mdl.intercept_]
for j in range(x_p):
    est_parms += [mdl.coef_[j]]
est_parms += [mse]
sample_list += [np.array(est_parms)]
St = chart.chart_stat(sample_list)
T2 = chart.T2_stat(St,t)
ooc = chart.check_ooc(St,t=t)

ml_newrow = pd.Series({'t': t+1,
                        'Parm': p,
                        'Delta': d,
                        'B0': sample_list[-1][0],
                        'B1': sample_list[-1][1],
                        'B2':sample_list[-1][2],
                        'S2':sample_list[-1][3],
                        'T2':T2,
                        'OOC':ooc})

ml_exmpl_df = pd.concat([ml_exmpl_df,ml_newrow.to_frame().T],ignore_index=True)
ml_exmpl_df.to_csv(ml_exmpl_filename,index=False,mode='w') #update csv file

print(ml_exmpl_df)

print("========================")
print("SIMULATIONS COMPLETED")
print("========================")