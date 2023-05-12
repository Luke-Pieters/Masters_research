import numpy as np

#==============================================================
#== MULTIVARIATE SCHEMES ======================================
#==============================================================

class SPM_Multi_chart:
    ''' 
    Statistical Process Monitoring Univariate scheme 
    @params:
        mean_0   - Optional  : IC mean of process (float) ; Defualts to 0
        sig2_0   - Optional  : IC variance of process (float) ; Defualts to 1
        L        - Optional  : CL parameter for chart_obj ; Defualts to None
        p        - Optional  : dimention of multivariate chart (int) ; Defualts to 2
    
        phi     - Optional : main smoothing parameter used by chart_object (float) ; should be in (0,1]
        phi2    - Optional : second smoothing parameter used by some charts (float) ; should be in [0,phi)
        k       - Optional : modified parameter used by modified charts (float) ; 

    @functions
         check_ooc          :
         T2_stat            :
         change_L           :
         change_parameters  :
    
    '''
    def __init__(self,mean_0=None,sig2_0=None,L=2.6,p=2,**paramaters) -> None:
        if mean_0 is None:
            self.mean = np.zeros(p)
        else:
            self.mean = np.array(mean_0)

        if sig2_0 is None:
            self.sig2 = np.diag(np.ones(p))
        else:
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

    def change_parameters(self,**paramaters):
        #phi and phi1 
        if "phi" in paramaters: 
            self.phi = paramaters["phi"]
            
        #phi2    
        if "phi2" in paramaters: 
            self.phi2 = paramaters["phi2"]
        
        #k for modified EWMA and HWMA  
        if "k" in paramaters: 
            self.k = paramaters["k"]

    def reset_chart(self):
        self.chart_history = [self.mean]

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


#Extended HWMA SCHEME    
class EHWMA(SPM_Multi_chart):
    def chart_stat(self,series) -> np.array:
        St = self.phi*series[-1] - self.phi2*series[-2] + (1-self.phi+self.phi2)*np.mean(series[:-1])
        self.chart_history = self.chart_history + [St]
        return St

    def chart_var(self,t) -> float:   
        if t ==1:
            return self.sig2*(self.phi**2)
        else:
            c1 = self.phi**2
            c2 = 1-self.phi- (t-2)*self.phi2
            c3 = t-1
            c4 = 1-self.phi +self.phi2
            c5=c3
            c6=t-2
            return (self.sig2)*(c1 + ((c2/c3)**2) + ((c4/c5)**2)*(c6))

#Modified HWMA SCHEME
class MHWMA(SPM_Multi_chart):
    def chart_stat(self,series) -> float:
        St = self.phi*series[-1] + (1-self.phi)*np.mean(series[:-1]) + self.k*(series[-1]-series[-2])
        self.chart_history = np.append(self.chart_history,St)
        return St

    def chart_var(self,t) -> float:   
        if t ==1:
            return self.sig2*((self.phi+self.k)**2)
        else:
            c1 = (self.phi+self.k)**2
            c2 = (1-self.phi)/(t-1)
            c3 = (c2 - self.k)**2
            c4 = (t-2)
            return (self.sig2)*(c1 + c3 + c4*(c2**2))

#EWMA SCHEME    
class EWMA(SPM_Multi_chart):
    def chart_stat(self,series) -> float:
        St = self.phi*series[-1] + (1-self.phi)*self.chart_history[-1]
        self.chart_history = self.chart_history + [St]
        return St

    def chart_var(self,t) -> float:   
        c1 = self.phi/(2-self.phi)
        c2 = 1 - ((1-self.phi)**(2*t))
        return (self.sig2)*c1*c2


#Extended EWMA SCHEME    
class EEWMA(SPM_Multi_chart):
    def chart_stat(self,series) -> float:
        St = self.phi*series[-1] - self.phi2*series[-2] + (1- self.phi + self.phi2)*self.chart_history[-1]
        self.chart_history = self.chart_history + [St]
        return St

    def chart_var(self,t) -> float:   
        c1 = np.longdouble((self.phi**2)+(self.phi2**2))
        c2 = np.longdouble(1 - (1- self.phi +self.phi2)**(2*t))
        c3 = np.longdouble(2*(self.phi-self.phi2) - ((self.phi-self.phi2)**2))
        c4 = np.longdouble(2*self.phi*self.phi2*(1-self.phi + self.phi2))
        c5 = np.longdouble(1- ((1-self.phi+self.phi2)**(2*t -2)))

        a1 = np.longdouble(c1*c2 - c4*c5)
        a2 = c3

        # print(a1,a2)

        return self.sig2*(a1/a2)


#Modified EWMA SCHEME    
class MEWMA(SPM_Multi_chart):
    def chart_stat(self,series) -> float:
        St = self.phi*series[-1] + (1-self.phi)*self.chart_history[-1] +self.k*(series[-1]-series[-2])
        self.chart_history = self.chart_history + [St]
        return St

    def chart_var(self,t) -> float:   
        c1 = self.phi + 2*self.phi*self.k + 2*(self.k**2)
        c2 = self.phi*((1-self.phi-self.k)**2)*((1-self.phi)**(2*t-2))
        c3 = 2 - self.phi

        return self.sig2*((c1-c2)/c3)


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