import spm_sim_module as sim
import Schemes_module as spm_schemes

#CHART TO TEST
chart = spm_schemes.MEWMA()
chart_name = chart.__class__.__name__

print("Chart: " + chart_name)

initial_L = 2.75

#CHART PARAMETERS 
phi = 0.1

# phi2_arr = 

k = 1

chart.change_parameters(phi=phi,k=k)

res = sim.spm_optimize_L(chart_obj=chart,initial_L=initial_L,n=10000,tol=1)

print(f'Optimal L for {chart_name}({phi},{k}):  {res}')