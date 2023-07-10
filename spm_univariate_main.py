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
n=50000
tau = 1 

#CHART TO TEST
chart = spm_schemes.EHWMA()
chart_name = chart.__class__.__name__

print("Chart: " + chart_name)

#SHIFT SIZES 
delta = np.arange(0,3.25,0.25)

print("Shift Sizes:")
print(delta)

#CHART PARAMETERS 
phi_arr = [0.1,0.25,0.5,0.9]

phi2_arr = {0.1: [0.01,0.05,0.09],
            0.25: [0.05,0.1,0.2],
            0.5: [0.1,0.2,0.4],
            0.9: [0.2,0.5,0.8]} 

# k_arr = [1,2,3,4,
#         1,2,3,4,
#         1,2,3,4]

use_k = False
opt_k = lambda x: -x/2

with open(f'results\{chart_name}_optimal_L.json') as json_file:
       L_arr = json.load(json_file)


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
    output_df = pd.DataFrame(columns=['ARL','SDRL','MRL','L','Phi','Phi2','Delta','Parameter_string'])

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
    output_df = pd.DataFrame(columns=['ARL','SDRL','MRL','L','Phi','k','Delta','Parameter_string'])    
else:
    #check parameters match chart
    accepted_charts = ["EWMA","HWMA"]
    if chart_name not in accepted_charts:
        log.warning('(!) Error: Chart and parameter mis-match')
        exit()

    #parameters
    sim_parameters = phi_arr

    #ouput df
    output_df = pd.DataFrame(columns=['ARL','SDRL','MRL','L','Phi','Delta','Parameter_string'])


print("Simulation Parameters:")
print(sim_parameters)

total_parameters = len(sim_parameters)

#Check L_arr Length
# if len(L_arr.values) != total_parameters:
#         log.warning('(!) Error: L array not correct length')
#         exit()

#setup and set folders to save results
filepath = "./results/univariate_results"
filename = filepath + "/" + chart_name + "_ARL_SDRL_MRL_results.csv"
makedirs(filepath, exist_ok=True) 

#==========================================================================
#SIMULATIONS
#==========================================================================
start_time = time()

for d in delta:
    #DISTRIBUTION TO SAMPLE FROM 
    dist = sts.norm(loc=d,scale=1)
    print('========================')
    print("Delta: {:.2f}".format(d))
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

        results = spm_sim.spm_iterate(chart_obj=chart,distribution=dist,n=n,tau=tau,standardise=False,L=L) #ARL,SDRL,MRL 

        print(results)

        if 'phi2_arr' in globals():
            newrow = pd.Series({'ARL':results['ARL'],
                                'SDRL':results['SDRL'],
                                'MRL':results['MRL'],
                                'L':L,
                                'Phi':phi,
                                'Phi2':phi2,
                                'Delta': d,
                                'Parameter_string': parm_str})
            
        elif use_k in globals():
            newrow = pd.Series({'ARL':results['ARL'],
                                'SDRL':results['SDRL'],
                                'MRL':results['MRL'],
                                'L':L,
                                'Phi':phi,
                                'k':k,
                                'Delta': d,
                                'Parameter_string': parm_str})
            
        else:
            newrow = pd.Series({'ARL':results['ARL'],
                                'SDRL':results['SDRL'],
                                'MRL':results['MRL'],
                                'L':L,
                                'Phi':phi,
                                'Delta': d,
                                'Parameter_string': parm_str})
    
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
