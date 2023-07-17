import spm_multivariate_sim_module as sim
import Multivariate_Schemes_module as spm_schemes
import logging
import numpy as np
import json
from numpy import round

from datetime import datetime
now = datetime.now()
current_time = now.strftime("%Y%m%d-h%H-%M-%S")

log = logging.getLogger(__name__)

logging.basicConfig(filename=f"logs/Log-{current_time}",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

#CHART TO TEST
p=4
chart = spm_schemes.MHWMA(p=p)
chart_name = chart.__class__.__name__

print("Chart: " + chart_name + f"p={p}")

#CHART PARAMETERS 
phi_arr = [0.1,0.25]

phi2_arr = {0.1: [0.01,0.05,0.09],
            0.25: [0.05,0.1,0.2],
            0.5: [0.1,0.2,0.4],
            0.9: [0.2,0.5,0.8]}

opt_k = lambda x: -x/2

phi_parm = []
# k_parm = []

with open(f'results\multivar_{chart_name}_optimal_L.json') as json_file:
    L_arr = json.load(json_file)

for phi in phi_arr:
    # for phi2 in phi2_arr[phi]:
        k = opt_k(phi)
        logging.info(f"Running Optimize for {chart_name}({phi})")
        chart.change_parameters(phi=phi,k=k)
        # chart.change_parameters(phi=phi,k=k)
        initial_L = L_arr[f"p={p}"][str(phi)]
        # initial_L = L_arr[f"p={p}"][str(phi)][str(phi2)]
        res = sim.spm_optimize_L(chart_obj=chart,initial_L=initial_L,n=50000,tol=1,p=p)
            
        logging.info(f'Optimal L for {chart_name}({phi}):  {res}')
        print(f'Optimal L for p{p} {chart_name}({phi}):  {res}')
        L_arr[f"p={p}"][str(phi)] = round(res[0],5)
        # L_arr[f"p={p}"][str(phi)][str(phi2)] = round(res[0],5)

        with open(f'results\multivar_{chart_name}_optimal_L.json', 'w') as json_file:
            json.dump(L_arr, json_file)

logging.info(f'Optimization Complete for {chart_name} p{p}')
print('Optimization Complete')
