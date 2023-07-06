import spm_multivariate_sim_module as sim
import Multivariate_Schemes_module as spm_schemes
import logging

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

print("Chart: " + chart_name)

initial_L = 13

#CHART PARAMETERS 
phi_arr = [0.1,0.25]

phi2_arr = {0.1: [0.01,0.05,0.09],
            0.25: [0.05,0.1,0.2],
            0.5: [0.1,0.2,0.4],
            0.9: [0.2,0.5,0.8]}

opt_k = lambda x: -x/2

phi_parm = []
# k_parm = []
L_value = []

for phi in phi_arr:
    #for phi2 in phi2_arr[phi]:
        k = opt_k(phi)
        logging.info(f"Running Optimize for Multivariate p={p} {chart_name}({phi},{k})")
        chart.change_parameters(phi=phi,k=k)
        res = sim.spm_optimize_L(chart_obj=chart,initial_L=initial_L,n=10000,tol=10,p=p)
            
        logging.info(f'Optimal L for {chart_name}({phi},{k}):  {res}')
        print(f'Optimal L for {chart_name}({phi},{k}):  {res}')

logging.info(f'Optimization Complete for Multivariate p={p} {chart_name}')
print('Optimization Complete')
