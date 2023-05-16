import spm_sim_module as sim
import Schemes_module as spm_schemes
import logging

from datetime import datetime
now = datetime.now()
current_time = now.strftime("%H-%M-%S")

log = logging.getLogger(__name__)

logging.basicConfig(filename=f"logs/Log-{current_time}",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

#CHART TO TEST
chart = spm_schemes.MHWMA()
chart_name = chart.__class__.__name__

print("Chart: " + chart_name)

initial_L = 2.75

#CHART PARAMETERS 
phi_arr = [0.5,0.9]

# phi2_arr = 

k_arr = [1,2,3,4,5]

phi_parm = []
k_parm = []
L_value = []

for phi in phi_arr:
    for k in k_arr:
        logging.info(f"Running Optimize for {chart_name}({phi},{k})")
        chart.change_parameters(phi=phi,k=k)
        res = sim.spm_optimize_L(chart_obj=chart,initial_L=initial_L,n=10000,tol=1)
        
        logging.info(f'Optimal L for {chart_name}({phi},{k}):  {res}')
        print(f'Optimal L for {chart_name}({phi},{k}):  {res}')





res = sim.spm_optimize_L(chart_obj=chart,initial_L=initial_L,n=10000,tol=1)

print(f'Optimal L for {chart_name}({phi},{k}):  {res}')