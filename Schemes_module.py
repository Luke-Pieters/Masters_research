import numpy as np

#==============================================================
#== UNIVARIATE SCHEMES ========================================
#==============================================================
class SPM_uni_chart:
    ''' 
    Statistical Process Monitoring Univariate scheme 
    @params:
        mean_0   - Optional  : IC mean of process (float) ; Defualts to 0
        sig2_0   - Optional  : IC variance of process (float) ; Defualts to 1
        L        - Optional  : CL parameter for chart_obj ; Defualts to None
    
        phi     - Optional : main smoothing parameter used by chart_object (float) ; should be in (0,1]
        phi2    - Optional : second smoothing parameter used by some charts (float) ; should be in [0,phi)
        k       - Optional : modified parameter used by modified charts (float) ; 

    @functions
         check_ooc          :
         lb_ub              :
         change_L           :
         change_parameters  :
    
    '''
    def __init__(self,mean_0=0,sig2_0=1,L=2.6,**paramaters) -> None:
        self.mean = mean_0
        self.sig2 = sig2_0 #var
        self.L = L
        self.chart_history = np.array([mean_0])
        #phi and phi1 
        if "phi" in paramaters: 
            self.phi = paramaters["phi"]
            
        #phi2    
        if "phi2" in paramaters: 
            self.phi2 = paramaters["phi2"]
        
        #k for modified EWMA and HWMA  
        if "k" in paramaters: 
            self.k = paramaters["k"]    

    def check_ooc(self,stat: float,t) -> bool:
        '''Given the value of t and the charting statistic at t, 
        return TRUE if process is OOC'''
        lb,ub = self.lb_ub(t=t)
        if (stat <= lb)|(stat>=ub):
            return True
        else:
            return False

    def lb_ub(self,t) -> np.array:
        '''Returns the lower- and upperbound of the control limits'''
        v = self.chart_var(t)
        lb = self.mean - self.L*np.sqrt(v)
        ub = self.mean + self.L*np.sqrt(v)

        return [lb,ub]

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
        self.chart_history = np.array([self.mean])



#HWMA SCHEME   
class HWMA(SPM_uni_chart):
    def chart_stat(self,series) -> float:
        St = self.phi*series[-1] + (1-self.phi)*np.mean(series[:-1])
        self.chart_history = np.append(self.chart_history,St)
        return St
    
    def chart_var(self,t) -> float:
        if t==1:
            return (self.phi**2)*(self.sig2)
        else:
            return ((self.phi**2) + (((1-self.phi)**2)/(t-1)))*(self.sig2)

#Extended HWMA SCHEME    
class EHWMA(SPM_uni_chart):
    def chart_stat(self,series) -> float:
        St = self.phi*series[-1] - self.phi2*series[-2] + (1-self.phi+self.phi2)*np.mean(series[:-1])
        self.chart_history = np.append(self.chart_history,St)
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
class MHWMA(SPM_uni_chart):
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
class EWMA(SPM_uni_chart):
    def chart_stat(self,series) -> float:
        St = self.phi*series[-1] + (1-self.phi)*self.chart_history[-1]
        self.chart_history = np.append(self.chart_history,St)
        return St

    def chart_var(self,t) -> float:   
        c1 = self.phi/(2-self.phi)
        c2 = 1 - ((1-self.phi)**(2*t))
        return (self.sig2)*c1*c2
  
#Extended EWMA SCHEME    
class EEWMA(SPM_uni_chart):
    def chart_stat(self,series) -> float:
        St = self.phi*series[-1] - self.phi2*series[-2] + (1- self.phi + self.phi2)*self.chart_history[-1]
        self.chart_history = np.append(self.chart_history,St)
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
class MEWMA(SPM_uni_chart):
    def chart_stat(self,series) -> float:
        St = self.phi*series[-1] + (1-self.phi)*self.chart_history[-1] +self.k*(series[-1]-series[-2])
        self.chart_history = np.append(self.chart_history,St)
        return St

    def chart_var(self,t) -> float:   
        c1 = self.phi + 2*self.phi*self.k + 2*(self.k**2)
        c2 = self.phi*((1-self.phi-self.k)**2)*((1-self.phi)**(2*t-2))
        c3 = 2 - self.phi

        return self.sig2*((c1-c2)/c3)
    
    
    
       


