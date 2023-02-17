import numpy as np
import pandas as pd
import spm_sim_module as spm_sim
import Schemes_module as spm_schemes
import scipy.stats as sts
from os import makedirs
import logging

logging.basicConfig(format='%(message)s')
log = logging.getLogger(__name__)
#==========================================================================
#SETUP
#==========================================================================

#ITERATE PARAMETERS
n=500
tau = 1

#CHART TO TEST
chart = spm_schemes.EEWMA()
chart_name = chart.__class__.__name__

print("Chart: " + chart_name)

#CHART PARAMETERS 
phi_arr = [0.1,0.2]

phi2_arr = [0.01,0.02,0.05,0.09,
            0.01,0.02,0.1,0.15]
            # 0.1,0.2,0.3,0.4,
            # 0.1,0.3,0.6,0.8]

# k_arr = [1,2,3,4,
#         1,2,3,4,
#         1,2,3,4,
#         1,2,3,4]

L_arr = [2.798]*8 #should be len= sum of (len of parameters)

#DISTRIBUTION TO SIMULATE FROM
dist = sts.norm(loc=0,scale=1)


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
    output_df = pd.DataFrame(columns=['ARL','SDRL','MRL','L','Phi','Phi2'])
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
    output_df = pd.DataFrame(columns=['ARL','SDRL','MRL','L','Phi','k'])    
else:
    #check parameters match chart
    accepted_charts = ["EWMA","HWMA"]
    if chart_name not in accepted_charts:
        log.warning('(!) Error: Chart and parameter mis-match')
        exit()

    #parameters
    sim_parameters = phi_arr

    #ouput df
    output_df = pd.DataFrame(columns=['ARL','SDRL','MRL','L','Phi'])


print("Simulation Parameters:")
print(sim_parameters)

total_parameters = len(sim_parameters)

#Check L_arr Length
if len(L_arr) != total_parameters:
        log.warning('(!) Error: L array not correct length')
        exit()

#==========================================================================
#SIMULATIONS
#==========================================================================
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


    results = spm_sim.spm_iterate(chart_obj=chart,distribution=dist,n=n,tau=tau) #ARL,SDRL,MRL 

    
    if 'phi2_arr' in globals():
        newrow = pd.Series({'ARL':results[0],
                            'SDRL':results[1],
                            'MRL':results[2],
                            'L':L_arr[i],
                            'Phi':parms_in_use[0],
                            'Phi2':parms_in_use[1]})
        output_df = pd.concat([output_df,newrow.to_frame().T],ignore_index=True)
    elif 'k_arr' in globals():
        newrow = pd.Series({'ARL':results[0],
                            'SDRL':results[1],
                            'MRL':results[2],
                            'L':L_arr[i],
                            'Phi':parms_in_use[0],
                            'k':parms_in_use[1]})
        output_df = pd.concat([output_df,newrow.to_frame().T],ignore_index=True)
    else:
        newrow = pd.Series({'ARL':results[0],
                            'SDRL':results[1],
                            'MRL':results[2],
                            'L':L_arr[i],
                            'Phi':parms_in_use})
        output_df = pd.concat([output_df,newrow.to_frame().T],ignore_index=True)

#==========================================================================
#PRINT RESULTS 
#==========================================================================
#setup and set folders to save results
filepath = "resulst/univariate_results"

makedirs(filepath, exist_ok=True) 

#save resulst 

#OUTPUT
print(output_df)

filename = filepath + "/" + chart_name + "_ARL_SDRL_MRL_results.csv"
output_df.to_csv(filename,index=False)  
