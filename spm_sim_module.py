import numpy as np
import scipy.stats as sts
import Schemes_module as spm


def spm_simulate(chart_obj,distribution,tau=1,mu_0=0,sig_0=1,max_it=1000):
    '''simulate for a chart with set parameters untill OOC, returns the first OOC t'''
    Xt= np.array([])
    Xt.append(mu_0) #X_0
    ooc = False
    t=0
    while (ooc==False) | (t<max_it):
        t += 1
        if t < tau:
            Xt.append(sts.norm(loc=mu_0,scale=sig_0).rvs(1))
            St = chart_obj.chart_stat(Xt)
        else:
            Xt.append(distribution.rvs(1))
            St = chart_obj.chart_stat(Xt)
            ooc = chart_obj.check_ooc(St,t=t)
            
    return t - tau +1 


def spm_iterate(n,chart_obj,distribution):
    '''iterate simulate function n times for set chart, return ARL,SDRL and MRL'''
    pass

def spm_optimize_h(chart_obj,n,initial_h,target_ARL=200,tol=0.01,max_its=100):
    '''run iteratations for set chart with set parameters and use 
    linear interpolation to itteratively find best h to achieve |ARL-target_ARL|<tol'''
    
    # linear interpolation:
    # x = X1 + (y-Y1)(X2-X1)/(Y2-Y1)
    # x = x to get y
    
    pass


#how to sample from distribution
#dist = sts.norm(loc=4,scale=1)
#arr = dist.rvs(size=1000,loc=10,scale=2)

#print(np.mean(arr))

#pull mean from dist
#dist.mean()
#dist.std()

