import numpy as np
import scipy.stats as sts
from scipy.optimize import minimize
import Schemes_module as spm
from time import time
from datetime import timedelta
from ProgressBar_module import printProgressBar

# Multivariate Simulate function
def spm_simulate(chart_obj,distribution,p=2,tau=1,mu_0=0,sig_0=1,max_it=1000):
    '''simulate for a multivariate chart with set parameters untill OOC, returns the first OOC t'''
    Xt = [np.array(mu_0)] #X_0
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
            sample_vec_standardised= (sample_vec-dist_mean)/dist_std
            Xt = Xt + [sample_vec_standardised]
            St = chart_obj.chart_stat(Xt)
            ooc = chart_obj.check_ooc(St,t=t)
            
    return t - tau +1


def spm_iterate(n,chart_obj,distribution,tau=1,L=None,p=2):
    '''iterate simulate function n times for set multivariate chart, return ARL,SDRL and MRL'''
    start_time = time()
    t_arr = np.array([])

    if (L!=None):
        chart_obj.change_L(new_L=L)
    
    printProgressBar(iteration=0,total=n,prefix='Iterate Progress')
    
    for i in range(n):
        printProgressBar(iteration=i,total=n,prefix='Iterate Progress')
        t_arr = np.append(t_arr,spm_simulate(chart_obj=chart_obj,distribution=distribution,tau=tau,p=p))
        
    ARL = np.mean(t_arr)
    SDRL = np.std(t_arr)
    MRL = np.median(t_arr)
    printProgressBar(iteration=n,total=n,prefix='Iterate Progress')
 
    run_time =np.round(time()-start_time+0.4,decimals=0)
    print("Time: {} ".format(timedelta(seconds=run_time)))
    
    return [ARL,SDRL,MRL]


def spm_optimize_h(chart_obj,n,p,initial_h,target_ARL=200,tol=1,max_its=1000,bounds=(0,3)):
    '''run iteratations for set chart with set parameters and use 
    linear interpolation to itteratively find best h to achieve |ARL-target_ARL|<tol'''
    start_time_op = time()
    #function to minimise
    f = lambda L : np.abs(target_ARL - spm_iterate(L=L,n=n,chart_obj=chart_obj,distribution=sts.norm(loc=0,scale=1),p=p)[0])

    min_func_results = minimize(fun=f,
                                x0=[initial_h],
                                method='Nelder-Mead',
                                tol=tol,
                                bounds=[bounds],
                                options={'maxiter':max_its,
                                        'disp':True,
                                        'return_all':True})
    
    run_time_op =np.round(time()-start_time_op+0.4,decimals=0)
    print("Optimization Time: {} ".format(timedelta(seconds=run_time_op)))

    return min_func_results.x