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
n = 10000

x_p = 2
x_names = [f"X{i+1}" for i in range(3)]
x_values = np.arange(-4,4.5,0.5)
x_n = len(x_values)
x_p = len(x_names)

true_parms = [3.0,2.0,5.0]
true_var = 1

change_parms = np.zeros(len(true_parms))
# delta_arr = [0, 0.5, 1.5, 3.0]
delta_arr = np.arange(0,3.25,0.25)
# delta_arr = [ 3.0]

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

sample_list = [0,0,0,0]
sample_list = [np.array(sample_list)]

mu_0 = sample_list[0]

print(sample_list)

opt_k = lambda x: -x/2


def sig_transformed(x,x_n,x_p,true_var):
    c1 = (x_n-x_p)*x
    c2= c1/true_var
    chi_prob=sts.chi2.cdf(c2,x_n-x_p)
    
    if chi_prob == 1:
        norm_q = 8
    else:
        norm_q = sts.norm.ppf(chi_prob,loc=0,scale=1)
    return norm_q


phi = 0.25
phi2 = 0.1
chart = spm_schemes.MHWMA(p=(x_p+2),phi=phi,phi2=phi2,k=opt_k(phi),mean_0=mu_0,sig2_0=True_sig)
chart_name = chart.__class__.__name__
print("Chart: " + chart_name)

with open(f'results\multivar_{chart_name}_optimal_L.json') as json_file:
       L_arr = json.load(json_file)

L = L_arr[str(f"p={4}")][str(phi)] 
# chart.change_L(L+18.6)
# L = L_arr[str(f"p={x_p+1}")][str(phi)][str(phi2)] 
print('L: ',L)
chart.change_L(L+12) #+9

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

ml_n = 100
# delta_arr = [ 0.5, 1.5, 3.0]
# delta_arr = [ 1.5, 3.0]

parm_names = {0:"B0",
              1:"B1",
              2:"B2",
              3:"S2"}

output_df = pd.DataFrame(columns=['Parm','Delta','ARL','SDRL','MRL','Phi'])
ml_df = pd.DataFrame(columns=['Parm','Delta','B0','B1','B2','S2','T2'])
ic_count = 0
# range(len(true_parms)+1)
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
            shift_vec = np.zeros(len(true_parms))
            shift_vec[p] = d*np.sqrt(True_sig[p,p]) 
            sim_parm = true_parms + shift_vec
            sim_var = 1 #actually std
        else:
            if d <= 1:
                continue
            sim_var = np.sqrt(true_var)*d #actually std
            sim_parm = true_parms
        t_arr = []
        print("="*30)
        print(f"Parmeter list: {[sim_parm] + [sim_var]}")
        print("="*30)
        printProgressBar(iteration=0,total=n,prefix='Simulation Progress')
        ml_counter = 0
        for i in range(n):
            ml_counter += 1
            if len(t_arr)>0:
                printProgressBar(iteration=i,total=n,prefix='Simulation Progress',printEnd="\n")
                print(f"{i}/{n} ARL: {np.mean(t_arr)} \033[F\033[F")
            sample_list = [0,0,0,0]
            sample_list = [np.array(sample_list)]
            t = 0
            ooc = False
            while ooc == False and t < 400:
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
                t_mse = float(sig_transformed(mse,x_n,x_p,true_var))
                # ln_mse = np.log(mse)

                est_parms = []
                for j in range(len(mdl.coef_)):
                    est_parms += [(mdl.coef_[j]-true_parms[j])/np.sqrt(true_var)]
                est_parms += [t_mse]
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
            
            if ml_counter <= ml_n:
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
        
        update_measures = {'Parm': p,
                            'ARL': ARL,
                            'SDRL': SDRL,
                            'MRL': MRL}
        
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
# #SHORT EXAMPLE DATA GENERATION 
# n = 5 #number of IC samples 

# sample_list = true_parms + [true_var]
# sample_list = [np.array(sample_list)]
# chart.reset_chart()

# ml_exmpl_df = pd.DataFrame(columns=['t','Parm','Delta','B0','B1','B2','S2'])

# filepath = "./results/pm/"
# # filename = filepath + "/" + chart_name + "_ARL_SDRL_MRL_results.csv"
# filename = filepath + "ml_exmpl_data.csv"
# makedirs(filepath, exist_ok=True)
# ooc = False

# d=0
# sim_parm = true_parms
# sim_var = 1
# p=-1
# for t in range(n):
#                 Y = 0
#                 for j in range(3):
#                     Y += sim_parm[j]*X_df[x_names[j]] 
#                 Y += sts.norm(loc=0,scale=sim_var).rvs(len(x_values))
                
#                 # print(Y)
#                 mdl = linear_model.LinearRegression(fit_intercept=False)
#                 mdl.fit(X_df,Y)
#                 y_hat = mdl.predict(X_df)
#                 mse = mean_squared_error(Y,y_hat)
#                 # ln_mse = np.log(mse)

#                 est_parms = []
#                 for j in range(len(mdl.coef_)):
#                     est_parms += [mdl.coef_[j]]
#                 est_parms += [mse]
#                 sample_list += [np.array(est_parms)]
#                 St = chart.chart_stat(sample_list)
#                 T2 = chart.T2_stat(St,t)
#                 ooc = chart.check_ooc(St,t=t)

#                 # print(f"t={t}",f"sample={est_parms}",f"St={St}",f"T2={T2}",f"L={chart.L}",f"ooc={ooc}")

#                 ml_newrow = pd.Series({'t': t+1,
#                                        'Parm': p,
#                                         'Delta': d,
#                                         'B0': sample_list[-1][0],
#                                         'B1': sample_list[-1][1],
#                                         'B2':sample_list[-1][2],
#                                         'S2':sample_list[-1][3]})
                
#                 ml_exmpl_df = pd.concat([ml_exmpl_df,ml_newrow.to_frame().T],ignore_index=True)
#                 ml_exmpl_df.to_csv(filename,index=False,mode='w') #update csv fil

# #ADD SMALL SHIFT TO PARM 1
# d=3
# p=1
# t+= 1
# shift_vec = change_parms
# shift_vec[p] = d*np.sqrt(true_var) 
# sim_parm = true_parms + shift_vec
# sim_var = true_var

# Y = sim_parm[0]
# for j in range(x_p):
#     Y += sim_parm[j+1]*X_df[x_names[j]] 
# Y += sts.norm(loc=0,scale=sim_var).rvs(len(x_values))

# # print(Y)
# mdl = linear_model.LinearRegression()
# mdl.fit(X_df,Y)
# y_hat = mdl.predict(X_df)
# mse = mean_squared_error(Y,y_hat)

# est_parms = [mdl.intercept_]
# for j in range(x_p):
#     est_parms += [mdl.coef_[j]]
# est_parms += [mse]
# sample_list += [np.array(est_parms)]
# St = chart.chart_stat(sample_list)
# T2 = chart.T2_stat(St,t)
# ooc = chart.check_ooc(St,t=t)

# ml_newrow = pd.Series({'t': t+1,
#                         'Parm': p,
#                         'Delta': d,
#                         'B0': sample_list[-1][0],
#                         'B1': sample_list[-1][1],
#                         'B2':sample_list[-1][2],
#                         'S2':sample_list[-1][3],
#                         'T2':T2,
#                         'OOC':ooc})

# ml_exmpl_df = pd.concat([ml_exmpl_df,ml_newrow.to_frame().T],ignore_index=True)
# ml_exmpl_df.to_csv(ml_exmpl_filename,index=False,mode='w') #update csv file

# #ADD medium SHIFT TO PARM 2
# d=2
# p=2
# t+= 1
# shift_vec = change_parms
# shift_vec[p] = d*np.sqrt(true_var) 
# sim_parm = true_parms + shift_vec
# sim_var = true_var

# Y = sim_parm[0]
# for j in range(x_p):
#     Y += sim_parm[j+1]*X_df[x_names[j]] 
# Y += sts.norm(loc=0,scale=sim_var).rvs(len(x_values))

# # print(Y)
# mdl = linear_model.LinearRegression()
# mdl.fit(X_df,Y)
# y_hat = mdl.predict(X_df)
# mse = mean_squared_error(Y,y_hat)

# est_parms = [mdl.intercept_]
# for j in range(x_p):
#     est_parms += [mdl.coef_[j]]
# est_parms += [mse]
# sample_list += [np.array(est_parms)]
# St = chart.chart_stat(sample_list)
# T2 = chart.T2_stat(St,t)
# ooc = chart.check_ooc(St,t=t)

# ml_newrow = pd.Series({'t': t+1,
#                         'Parm': p,
#                         'Delta': d,
#                         'B0': sample_list[-1][0],
#                         'B1': sample_list[-1][1],
#                         'B2':sample_list[-1][2],
#                         'S2':sample_list[-1][3],
#                         'T2':T2,
#                         'OOC':ooc})

# ml_exmpl_df = pd.concat([ml_exmpl_df,ml_newrow.to_frame().T],ignore_index=True)
# ml_exmpl_df.to_csv(ml_exmpl_filename,index=False,mode='w') #update csv file

# #ADD large SHIFT TO VAR
# d=1
# p=3
# t+= 1 
# sim_parm = true_parms 
# sim_var = (1 + d)*2

# Y = sim_parm[0]
# for j in range(x_p):
#     Y += sim_parm[j+1]*X_df[x_names[j]] 
# Y += sts.norm(loc=0,scale=sim_var).rvs(len(x_values))

# # print(Y)
# mdl = linear_model.LinearRegression()
# mdl.fit(X_df,Y)
# y_hat = mdl.predict(X_df)
# mse = mean_squared_error(Y,y_hat)

# est_parms = [mdl.intercept_]
# for j in range(x_p):
#     est_parms += [mdl.coef_[j]]
# est_parms += [mse]
# sample_list += [np.array(est_parms)]
# St = chart.chart_stat(sample_list)
# T2 = chart.T2_stat(St,t)
# ooc = chart.check_ooc(St,t=t)

# ml_newrow = pd.Series({'t': t+1,
#                         'Parm': p,
#                         'Delta': d,
#                         'B0': sample_list[-1][0],
#                         'B1': sample_list[-1][1],
#                         'B2':sample_list[-1][2],
#                         'S2':sample_list[-1][3],
#                         'T2':T2,
#                         'OOC':ooc})

# ml_exmpl_df = pd.concat([ml_exmpl_df,ml_newrow.to_frame().T],ignore_index=True)
# ml_exmpl_df.to_csv(ml_exmpl_filename,index=False,mode='w') #update csv file

# print(ml_exmpl_df)

print("========================")
print("SIMULATIONS COMPLETED")
print("========================")