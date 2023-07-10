import spm_sim_module as sim
import Schemes_module as spm_schemes
import logging
import json

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
chart = spm_schemes.HWMA()
chart_name = chart.__class__.__name__

print("Chart: " + chart_name)

initial_L = 2.5

#CHART PARAMETERS 
phi_arr = [0.1,0.25,0.5,0.9]
# phi2_arr = {0.5: [0.1,0.2,0.4],
#             0.9: [0.2,0.5,0.8]} 

opt_k = lambda x: -x/2

phi_parm = []
# k_parm = []
L_value = []

with open(f'results\{chart_name}_optimal_L.json') as json_file:
    L_arr = json.load(json_file)

for phi in phi_arr:
    k = opt_k(phi)
    logging.info(f"Running Optimize for {chart_name}({phi},{k})")
    chart.change_parameters(phi=phi,k=k)
    initial_L = L_arr[str(phi)]
    # initial_L = L_arr[str(phi)][str(phi2)]
    res = sim.spm_optimize_L(chart_obj=chart,initial_L=initial_L,n=50000,tol=1)
        
    logging.info(f'Optimal L for {chart_name}({phi},{k}):  {res}')
    print(f'Optimal L for {chart_name}({phi},{k}):  {res}')
    L_arr[str(phi)] = res[0]

with open(f'results\{chart_name}_optimal_L.json', 'w') as json_file:
    json.dump(L_arr, json_file)

logging.info(f'Optimization Complete for {chart_name}')
print('Optimization Complete')
