import numpy as np
import scipy.stats as sts
from scipy.optimize import minimize
import Schemes_module as spm
from time import time
from datetime import timedelta
from ProgressBar_module import printProgressBar


def spm_simulate(chart_obj,distribution,tau=1,mu_0=0,sig_0=1,max_it=1000,standardise=False):
    '''
    simulate for a chart with set parameters untill OOC, returns the number of samples untill first OOC signal t.

    @params:
        chart_obj       - Required  : current iteration (SPM_chart Object)
        distribution    - Required  : scipy.stats distribution with rvs operation 
        tau             - Optional  : conditional delay parameter (int) ; Defualts to 1 (Zero state)
        mu_0            - Optional  : IC mean of process (float) ; Defualts to 0
        sig_0           - Optional  : IC std of process (float) ; Defualts to 1
        max_it          - Optional  : maximum number of samples that will be taken (int) ; Defualts to 1000
        standardise     - Optional  : Standardise samples using the mean and std of ditribution (bool) ; Defualt is False

    @Returns:
        t - tau +1 
    '''
    Xt= []
    Xt = Xt + [mu_0] #X_0
    ooc = False
    t=0
    dist_mean = distribution.mean()
    dist_std = distribution.std()

    chart_obj.reset_chart()

    while (ooc==False) & (t<max_it):
        t += 1
        if t < tau:
            sample = sts.norm(loc=mu_0,scale=sig_0).rvs(1)
            Xt = Xt + [sample[0]]
            St = chart_obj.chart_stat(Xt)
        else:
            #sample from given distribution, and standardise
            if standardise:
                sample = (distribution.rvs(1)-dist_mean)/dist_std
                Xt = Xt + [sample[0]]
            else:    
                sample = distribution.rvs(1)
                Xt = Xt + [sample[0]]
            St = chart_obj.chart_stat(series=Xt)
            ooc = chart_obj.check_ooc(stat=St,t=t)
            
    return (t - tau +1)  


def spm_iterate(n,chart_obj,distribution,tau=1,L=None,standardise=False,seed=123):
    '''
    iterate simulate function n times for set chart, return ARL,SDRL and MRL
    
    @params:
        n               - Required  : number of iterations to run (int)
        chart_obj       - Required  : current iteration (SPM_chart Object)
        distribution    - Required  : scipy.stats distribution with rvs operation 
        tau             - Optional  : conditional delay parameter (int) ; Defualts to 1 (Zero state)
        L               - Optional  : CL parameter for chart_obj ; Defualts to None
        standardise     - Optional  : Standardise samples using the mean and std of ditribution (bool) ; Defualt is False

    @Returns:
        [ARL,SDRL,MRL]
    '''
    start_time = time()
    t_arr = []
    np.random.seed(seed=seed)
    if (L!=None):
        chart_obj.change_L(new_L=L)
    
    printProgressBar(iteration=0,total=n,prefix='Iterate Progress')
    
    for i in range(n):
        printProgressBar(iteration=i,total=n,prefix='Iterate Progress')
        sim_t = spm_simulate(chart_obj=chart_obj,distribution=distribution,tau=tau,standardise=standardise)
        t_arr = t_arr + [sim_t]
        
    ARL = np.mean(t_arr)
    SDRL = np.std(t_arr)
    MRL = np.median(t_arr)
    MIN = np.min(t_arr)
    MAX = np.max(t_arr)
    Q25 = np.quantile(t_arr,0.25)
    Q75 = np.quantile(t_arr,0.75)
    printProgressBar(iteration=n,total=n,prefix='Iterate Progress')
 
    run_time =np.round(time()-start_time+0.4,decimals=0)
    print("Time: {} ".format(timedelta(seconds=run_time)))
    
    return {'ARL':ARL,'SDRL':SDRL,'MRL':MRL,'MIN':MIN,'MAX':MAX,'Q25':Q25,'Q75':Q75}
    # print(len(xt_arr))
    # return t_arr,xt_arr
        
    

def spm_optimize_L(chart_obj,n,initial_L,target_ARL=200,tol=1,max_its=1000,bounds=(0,5)):
    '''
    run iteratations for set chart with set parameters and use mimimize to find best L to achieve |ARL-target_ARL|<tol
    
    @params:
        chart_obj       - Required  : current iteration (SPM_chart Object)
        n               - Required  : number of iterations to run (int) 
        initial_L       - Required  : initial starting value for L (float)
        target_ARL      - Optional  : Target IC ARL value (float) ; Defualts to 200
        tol             - Optional  : Tollarance of minimise function (float) ; Defualts to 1
        max_it          - Optional  : maximum number of iterations that the miminise function will run (int) ; Defualts to 10
        bounds          - Optional  : upper and lower bound for valid L values (touple) ; Defualts to (0,3)

    @Returns:
        L
    '''
    start_time_op = time()
    #function to minimise
    f = lambda L : np.abs(target_ARL - spm_iterate(L=L,n=n,chart_obj=chart_obj,distribution=sts.norm(loc=0,scale=1))['ARL'])

    min_func_results = minimize(fun=f,
                                x0=[initial_L],
                                method='Nelder-Mead',
                                tol=tol,
                                bounds=[bounds],
                                options={'maxiter':max_its,
                                        'disp':True,
                                        'return_all':True})
    
    run_time_op =np.round(time()-start_time_op+0.4,decimals=0)
    print("Optimization Time: {} ".format(timedelta(seconds=run_time_op)))

    return min_func_results.x

# linear interpolation:
# x = X1 + (y-Y1)(X2-X1)/(Y2-Y1)
# x = x to get y


#how to sample from distribution
# dist = sts.norm(loc=0,scale=1)
#arr = dist.rvs(size=1000,loc=10,scale=2)

#print(np.mean(arr))

#pull mean from dist
#dist.mean()
# #dist.std()

# test_chart = spm.EWMA(L=2.794,phi=0.1,phi2=0.01)
# dist = sts.norm(loc=0,scale=1)

# # first_t = spm_simulate(chart_obj=test_chart,distribution=dist,tau=1,max_it=2)
# # print(first_t)

# m = spm_iterate(n=1000,chart_obj=test_chart,distribution=dist,seed=321)
# # m = spm_optimize_h(n=500,chart_obj=test_chart,initial_h=2.6,tol=1,max_its=5)
# print(m)



#from scipy.optimize import show_options
#show_options(solver='minimize',method="Nelder-Mead")