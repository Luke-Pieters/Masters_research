import numpy as np
import pandas as pd
import spm_sim_module as spm_sim
import Schemes_module as spm_schemes
import scipy.stats as sts
from os import makedirs
import logging
from time import time
from datetime import timedelta
import json

logging.basicConfig(format='%(message)s')
log = logging.getLogger(__name__)
#==========================================================================
#UNIVARIATE SIMULATIONS
#==========================================================================

#==========================================================================
#SETUP
#==========================================================================

#ITERATE PARAMETERS
n=10000
tau = 1 
# tau_arr = [1]
# tau_arr1 = [10]*5
# tau_arr1 = [tau_arr1[i]**(i) for i in range(5)]
# tau_arr2 = [x*2 for x in tau_arr1]
# tau_arr = [None]*(len(tau_arr1) + len(tau_arr2))
# tau_arr[::2] = tau_arr1
# tau_arr[1::2] = tau_arr2

# tau_arr = np.arange(1,110,10)

dist_arr = [sts.norm(loc=0,scale=1),
            sts.t(df=10),
            sts.gamma(a=1,scale=1),
            sts.gamma(a=10,scale=1),
            sts.lognorm(scale=np.exp(0),s=1),
            sts.chi2(df=30)]
dist_names = ["N(0,1)","t(10)","GAM(1,1)","GAM(10,1)","LogN(0,1)","X2(30)"]
dist_num = len(dist_arr)
# print(tau_arr)

#CHART TO TEST
chart = spm_schemes.EHWMA()
chart_name = chart.__class__.__name__

print("Chart: " + chart_name)

#SHIFT SIZES 
# delta = np.arange(0,3.25,0.25)
# delta = [0.25,3.0]
delta = [0]
print("Shift Sizes:")
print(delta)

#CHART PARAMETERS 
phi_arr = [0.1,0.25]
# phi_arr = [0.1,0.25,0.5,0.9]

phi2_arr = {0.1: [0.01,0.05,0.09],
            0.25: [0.05,0.1,0.2],
            0.5: [0.1,0.2,0.4],
            0.9: [0.2,0.5,0.8]} 


use_k = False   
opt_k = lambda x: -x/2

with open(f'results\{chart_name}_optimal_L.json') as json_file:
       L_arr = json.load(json_file)

df_cols = ['Tau','ARL','SDRL','MRL','MIN','MAX','Q25','Q75','L','Phi','Delta','Parameter_string','Distribution']

if 'phi2_arr' in globals():
    #check parameters match chart
    accepted_charts = ["EEWMA","EHWMA"]
    if chart_name not in accepted_charts:
        log.warning('(!) Error: Chart and parameter mis-match')
        exit()

    #parameters 
    sim_parameters = []
    for phi in phi_arr:
        for phi2 in phi2_arr[phi]:
            sim_parameters += [[phi,phi2]]

    #ouput df
    # output_df = pd.DataFrame(columns=['ARL','SDRL','MRL','L','Phi','Phi2','Delta','Parameter_string'])
    df_cols += ['Phi2']
    output_df = pd.DataFrame(columns=df_cols)

elif use_k:
    #check parameters match chart
    accepted_charts = ["MEWMA","MHWMA"]
    if chart_name not in accepted_charts:
        log.warning('(!) Error: Chart and parameter mis-match')
        exit()

    #parameters
    sim_parameters = []
    for phi in phi_arr:
        sim_parameters += [[phi,opt_k(phi)]]

    #ouput df
    # output_df = pd.DataFrame(columns=['ARL','SDRL','MRL','L','Phi','k','Delta','Parameter_string'])    
    df_cols += ['k']
    output_df = pd.DataFrame(columns=df_cols)   
else:
    #check parameters match chart
    accepted_charts = ["EWMA","HWMA"]
    if chart_name not in accepted_charts:
        log.warning('(!) Error: Chart and parameter mis-match')
        exit()

    #parameters
    sim_parameters = phi_arr

    #ouput df
    # output_df = pd.DataFrame(columns=['ARL','SDRL','MRL','L','Phi','Delta','Parameter_string'])
    output_df = pd.DataFrame(columns=df_cols)


print("Simulation Parameters:")
print(sim_parameters)

total_parameters = len(sim_parameters)

#Check L_arr Length
# if len(L_arr.values) != total_parameters:
#         log.warning('(!) Error: L array not correct length')
#         exit()

#setup and set folders to save results
# filepath = "./results/univariate_results/"
filepath = "./results/univariate_results/dist/"
# filename = filepath + "/" + chart_name + "_ARL_SDRL_MRL_results.csv"
filename = filepath + "/" + chart_name + "_dist_results_std.csv"
makedirs(filepath, exist_ok=True) 

#==========================================================================
#SIMULATIONS
#==========================================================================
start_time = time()

for d in delta:
    for dist_i in range(dist_num):
        #DISTRIBUTION TO SAMPLE FROM 
        dist = dist_arr[dist_i]
        # dist = sts.norm(loc=d,scale=1)
        print('========================')
        print(f"Delta: {d}, Dist: {dist_names[dist_i]}")
        print('========================')
        for i in range(total_parameters):
            parms_in_use = sim_parameters[i]
            
            #select parameters
            if 'phi2_arr' in globals():
                phi = parms_in_use[0]
                phi2 = parms_in_use[1]
                L = L_arr[str(phi)][str(phi2)]
                chart.change_parameters(phi=phi,phi2=phi2)
                print(f"Parameters: Phi: {phi}, Phi2: {phi2}, L: {L}")
                parm_str = f'phi={phi},phi2={phi2}'
            elif use_k:
                phi = parms_in_use[0]
                k = parms_in_use[1]
                L = L_arr[str(phi)]
                chart.change_parameters(phi=phi,k=k)
                print(f"Parameters: Phi: {phi}, K: {k}, L: {L}")
                parm_str = f'phi={phi},k={k}'
            else:
                phi = parms_in_use
                L = L_arr[str(phi)]
                chart.change_parameters(phi=phi)  
                print(f"Parameters: Phi: {phi}, L: {L}") 
                parm_str = f'phi={phi}'

            results = spm_sim.spm_iterate(chart_obj=chart,distribution=dist,n=n,tau=tau,standardise=True,L=L) #ARL,SDRL,MRL 

            print(results)
            
            newrow = {'Tau': tau,
                        'ARL':results['ARL'],
                        'SDRL':results['SDRL'],
                        'MRL':results['MRL'],
                        'MIN':results['MIN'],
                        'MAX':results['MAX'],
                        'Q25':results['Q25'],
                        'Q75':results['Q75'],
                        'L':L,
                        'Phi':phi,
                        'Delta':d,
                        'Parameter_string':parm_str,
                        'Distribution':dist_names[dist_i]}

            if 'phi2_arr' in globals():
                newrow['Phi2'] = phi2
                
            elif use_k in globals():
                newrow['k'] = k

            newrow = pd.Series(newrow)
            output_df = pd.concat([output_df,newrow.to_frame().T],ignore_index=True)
            output_df.to_csv(filename,index=False,mode='w') #update csv file 

#==========================================================================
#PRINT RESULTS 
#==========================================================================

#save results 

run_time =np.round(time()-start_time+0.4,decimals=0)
print("Total Run-Time: {} ".format(timedelta(seconds=run_time)))

#OUTPUT
print(output_df)

# filename = filepath + "/" + chart_name + "_ARL_SDRL_MRL_results.csv"
# output_df.to_csv(filename,index=False)  

print("Output DataFrame saved to: " + filename)

print("========================")
print("SIMULATIONS COMPLETED")
print("========================")
