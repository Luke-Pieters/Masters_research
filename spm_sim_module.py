import numpy as np


def spm_simulate(mu_1,sig_1,chart_obj):
    '''simulate for a chart with set parameters untill OOC, returns the first OOC t'''
    pass

def spm_itterate(n,chart_obj):
    '''itterate simulate function n times for set chart, return ARL,SDRL and MRL'''
    pass

def spm_optimize_h(initial_h,target_ARL=200,tol=0.01,max_its=100):
    '''run itterations for set chart with set parameters and use linear interpolation to itteratively find best h to achieve |ARL-target_ARL|<tol'''
    pass

