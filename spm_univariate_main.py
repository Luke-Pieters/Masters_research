import numpy as np
import pandas as pd
import spm_sim_module as spm_sim
import Schemes_module as spm_schemes
import scipy.stats as sts
from os import makedirs
import logging
from time import time
from datetime import timedelta

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

#CHART TO TEST
chart = spm_schemes.EWMA()
chart_name = chart.__class__.__name__

print("Chart: " + chart_name)

#SHIFT SIZES 
delta = [0]
# delta = [0,0.25]
# delta = np.arange(0,3.25,0.25)

print("Shift Sizes:")
print(delta)

#CHART PARAMETERS 
phi_arr = [0.1,0.25,0.5]

# phi2_arr = [0.01,0.02,0.05,0.09,
#             0.01,0.02,0.1,0.15,
#              0.1,0.2,0.3,0.4]


# k_arr = [1,2,3,4,
#         1,2,3,4,
#         1,2,3,4]

L_arr = [2.483,
2.687,
2.778]

# 2.772,
# 2.763,
# 2.762,
# 2.804,
# 2.803,
# 2.794,
# 2.804,
# 2.809,
# 2.801,
# ] #should be len= sum of (len of parameters)

#DISTRIBUTION TO SIMULATE FROM
# dist = sts.norm(loc=0,scale=1)


if 'phi2_arr' in globals():
    #check parameters match chart
    accepted_charts = ["EEWMA","EHWMA"]
    if chart_name not in accepted_charts:
        log.warning('(!) Error: Chart and parameter mis-match')
        exit()

    #parameters 
    sim_parameters = np.repeat(phi_arr,4)
    sim_parameters = np.stack([sim_parameters,phi2_arr],axis=-1)

    #ouput df
    output_df = pd.DataFrame(columns=['ARL','SDRL','MRL','L','Phi','Phi2','Delta'])

elif 'k_arr' in globals():
    #check parameters match chart
    accepted_charts = ["MEWMA","MHWMA"]
    if chart_name not in accepted_charts:
        log.warning('(!) Error: Chart and parameter mis-match')
        exit()

    #parameters
    sim_parameters = np.repeat(phi_arr,4)
    sim_parameters = np.stack([sim_parameters,k_arr],axis=-1)

    #ouput df
    output_df = pd.DataFrame(columns=['ARL','SDRL','MRL','L','Phi','k','Delta'])    
else:
    #check parameters match chart
    accepted_charts = ["EWMA","HWMA"]
    if chart_name not in accepted_charts:
        log.warning('(!) Error: Chart and parameter mis-match')
        exit()

    #parameters
    sim_parameters = phi_arr

    #ouput df
    output_df = pd.DataFrame(columns=['ARL','SDRL','MRL','L','Phi','Delta'])


print("Simulation Parameters:")
print(sim_parameters)

total_parameters = len(sim_parameters)

#Check L_arr Length
if len(L_arr) != total_parameters:
        log.warning('(!) Error: L array not correct length')
        exit()

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
        
        if 'phi2_arr' in globals():
            chart.change_parameters(phi=parms_in_use[0],phi2=parms_in_use[1])
            print("Parameters:","Phi: {:.2f}".format(parms_in_use[0]),"Phi2: {:.2f}".format(parms_in_use[1]),"L: {:.2f}".format(L_arr[i]))
        elif 'k_arr' in globals():
            chart.change_parameters(phi=parms_in_use[0],k=parms_in_use[1])
            print("Parameters:","Phi: {:.2f}".format(parms_in_use[0]),"k: {:.2f}".format(parms_in_use[1]),"L: {:.2f}".format(L_arr[i]))
        else:
            chart.change_parameters(phi=parms_in_use)  
            print("Parameters:","Phi: {:.2f}".format(parms_in_use),"L: {:.2f}".format(L_arr[i])) 


        results = spm_sim.spm_iterate(chart_obj=chart,distribution=dist,n=n,tau=tau,standardise=False,L=L_arr[i]) #ARL,SDRL,MRL 

        print(results)

        if 'phi2_arr' in globals():
            newrow = pd.Series({'ARL':results['ARL'],
                                'SDRL':results['SDRL'],
                                'MRL':results['MRL'],
                                'L':L_arr[i],
                                'Phi':parms_in_use[0],
                                'Phi2':parms_in_use[1],
                                'Delta': d})
            output_df = pd.concat([output_df,newrow.to_frame().T],ignore_index=True)
        elif 'k_arr' in globals():
            newrow = pd.Series({'ARL':results['ARL'],
                                'SDRL':results['SDRL'],
                                'MRL':results['MRL'],
                                'L':L_arr[i],
                                'Phi':parms_in_use[0],
                                'k':parms_in_use[1],
                                'Delta': d})
            output_df = pd.concat([output_df,newrow.to_frame().T],ignore_index=True)
        else:
            newrow = pd.Series({'ARL':results['ARL'],
                                'SDRL':results['SDRL'],
                                'MRL':results['MRL'],
                                'L':L_arr[i],
                                'Phi':parms_in_use,
                                'Delta': d})
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
