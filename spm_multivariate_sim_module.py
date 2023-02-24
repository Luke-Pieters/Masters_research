import numpy as np
import scipy.stats as sts
from scipy.optimize import minimize
import Multivariate_Schemes_module as spm
from time import time
from datetime import timedelta
from ProgressBar_module import printProgressBar

# Multivariate Simulate function
def spm_simulate(chart_obj,distribution,p=2,tau=1,mu_0=0,sig_0=1,max_it=1000,standardise=False)-> int:
    '''
    simulate for a multivariate chart with set parameters untill OOC, returns the number of samples untill first OOC signal t.

    @params:
        chart_obj       - Required  : current iteration (SPM_chart Object)
        distribution    - Required  : scipy.stats distribution with rvs operation 
        p               - Optional  : dimention of samples (int) ; Defualts to 2
        tau             - Optional  : conditional delay parameter (int) ; Defualts to 1 (Zero state)
        mu_0            - Optional  : IC mean of process (float) ; Defualts to 0
        sig_0           - Optional  : IC std of process (float) ; Defualts to 1
        max_it          - Optional  : maximum number of samples that will be taken (int) ; Defualts to 1000
        standardise     - Optional  : Standardise samples using the mean and std of ditribution (bool) ; Defualt is False

    @Returns:
        t - tau +1 
    '''
    Xt = [chart_obj.mean] #X_0
    ooc = False
    t=0
    dist_mean = distribution.mean()
    dist_std = distribution.std()
    while (ooc==False) & (t<max_it):
        t += 1
        if t < tau:
            sample_vec = sts.norm(loc=mu_0,scale=sig_0).rvs(p)
            Xt = Xt + [sample_vec]
            St = chart_obj.chart_stat(Xt)
        else:
            #sample from given distribution, and standardise
            sample_vec = distribution.rvs(p)
            if standardise:
                sample_vec_standardised= (sample_vec-dist_mean)/dist_std
            else: 
                sample_vec_standardised= sample_vec

            Xt = Xt + [sample_vec_standardised]
            St = chart_obj.chart_stat(Xt)
            ooc = chart_obj.check_ooc(St,t=t)
            
    return t - tau +1


def spm_iterate(n,chart_obj,distribution,p=2,tau=1,L=None,standardise=False)-> list:
    '''
    iterate simulate function n times for set multivariate chart, return ARL,SDRL and MRL
    
    @params:
        n               - Required  : number of iterations to run (int)
        chart_obj       - Required  : current iteration (SPM_chart Object)
        distribution    - Required  : scipy.stats distribution with rvs operation 
        p               - Optional  : dimention of samples (int) ; Defualts to 2
        tau             - Optional  : conditional delay parameter (int) ; Defualts to 1 (Zero state)
        L               - Optional  : CL parameter for chart_obj ; Defualts to None
        standardise     - Optional  : Standardise samples using the mean and std of ditribution (bool) ; Defualt is False

    @Returns:
        [ARL,SDRL,MRL]
    '''
    start_time = time()
    t_arr = np.array([])

    if (L!=None):
        chart_obj.change_L(new_L=L)
    
    printProgressBar(iteration=0,total=n,prefix='Iterate Progress')
    
    for i in range(n):
        printProgressBar(iteration=i,total=n,prefix='Iterate Progress')
        t_arr = np.append(t_arr,spm_simulate(chart_obj=chart_obj,distribution=distribution,tau=tau,p=p,standardise=standardise))
        
    ARL = np.mean(t_arr)
    SDRL = np.std(t_arr)
    MRL = np.median(t_arr)
    printProgressBar(iteration=n,total=n,prefix='Iterate Progress')
 
    run_time =np.round(time()-start_time+0.4,decimals=0)
    print("Time: {} ".format(timedelta(seconds=run_time)))
    
    return [ARL,SDRL,MRL]


def spm_optimize_L(chart_obj,n,p,initial_L,target_ARL=200,tol=1,max_its=10,bounds=(0,3))-> float:
    '''
    run iteratations for set chart with set parameters and use mimimize to find best L to achieve |ARL-target_ARL|<tol
    
    @params:
        chart_obj       - Required  : current iteration (SPM_chart Object)
        n               - Required  : number of iterations to run (int) 
        p               - Required  : dimention of samples (int) ; Defualts to 2
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
    f = lambda L : np.abs(target_ARL - spm_iterate(L=L,n=n,chart_obj=chart_obj,distribution=sts.norm(loc=0,scale=1),p=p)[0])

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


p=4

a=[1,2]


test_chart = spm.EHWMA(L=2.794,phi=0.1,phi2=0.01,p=p)
dist = sts.norm(loc=0,scale=1)

first_t = spm_simulate(chart_obj=test_chart,distribution=dist,tau=1,max_it=2,p=4)
print(first_t)
print(test_chart.chart_history)