import numpy as np

#==============================================================
#== Multivariate SCHEMES ======================================
#==============================================================

class SPM_Multi_chart:
    ''' 
    Statistical Process Monitoring Univariate scheme 
    @params:
        mean_0  : IC mean vector
        sig2_0  : Covariance matrix 
        L       : Bound for T2 statistic 
    
        (Optional)
    
        phi     :
        phi2    : 
        k       :    
    
    '''
    def __init__(self,mean_0,sig2_0,L,p,**paramaters) -> None:
        self.mean = np.array(mean_0)
        self.sig2 = np.array(sig2_0)
        self.L = L
        self.p=p
        self.chart_history = [self.mean] # use chart_history + [new_chart]
        #phi and phi1 
        if "phi" in paramaters: 
            self.phi = paramaters["phi"]
            
        #phi2    
        if "phi2" in paramaters: 
            self.phi2 = paramaters["phi2"]
        
        #k for modified EWMA and HWMA  
        if "k" in paramaters: 
            self.k = paramaters["k"]    

    def check_ooc(self, stat: np.array, t: int) -> bool:
        '''Given the value of t and the charting statistic at t, 
        return TRUE if process is OOC'''
        T2 = self.T2_stat(stat=stat,t=t)
        if (T2 >= self.L):
            return True
        else:
            return False

    def T2_stat(self, stat, t) -> np.array:
        '''Returns the T^2 statistic at time t'''
        V = self.chart_var(t) #should be matrix
        V_in = np.linalg.inv(V)
        c1 = (stat-self.mean) #vector

        T2 = c1.T@V_in@c1

        return T2

    def change_L(self,new_L):
        self.L = new_L

#HWMA SCHEME   
class HWMA(SPM_Multi_chart):
    def chart_stat(self,series) -> np.array:
        #series should be list of vectors/arrays
        St = self.phi*series[-1] + (1-self.phi)*np.mean(series[:-1])
        self.chart_history = self.chart_history + [St]
        return St
    
    def chart_var(self,t) -> np.array:
        if t==1:
            return (self.phi**2)*(self.sig2)
        else:
            return ((self.phi**2) + (((1-self.phi)**2)/(t-1)))*(self.sig2)

#TESTS
# m = [1,2,3]
# a= [m]
# b= a +[m]

# print(a,b)

# import scipy.stats as sts
# s2 = np.diag([1,1,1])
# dist = sts.norm(loc=0,scale=1)
# test_chart = HWMA([0,0,0],sig2_0=s2,L=2.6,phi=0.1,p=3)

# X = [[0,0,0]]
# X = X + [dist.rvs(size=3)]

# print("X1: ",X[-1])

# S1 = test_chart.chart_stat(X)

# X = X + [dist.rvs(size=3)]

# print("X2: ",X[-1])

# S2 = test_chart.chart_stat(X)

# print("S1,S2: ",S1, S2)
# print(test_chart.chart_history)

# T2 = test_chart.T2_stat(S2,2)
# ooc = test_chart.check_ooc(S2,t=2)

# print("T2: ",T2)
# print("OOC: ",ooc)