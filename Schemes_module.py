import numpy as np

#==============================================================
#== UNIVARIATE SCHEMES ========================================
#==============================================================
class SPM_uni_chart:
    ''' 
    Statistical Process Monitoring Univariate scheme 
    
    mean_0 : 
    sig2_0 : 
    
    Optional:
    
    phi :
    phi2: 
    k   : 
    
    '''
    def __init__(self,mean_0,sig2_0,**paramaters) -> None:
        self.mean = mean_0
        self.sig2 = sig2_0
        
        #phi and phi1 
        if "phi" in paramaters: 
            self.phi = paramaters["phi"]
            
        #phi2    
        if "phi2" in paramaters: 
            self.phi2 = paramaters["phi2"]
        
        #k for modified EWMA and HWMA  
        if "k" in paramaters: 
            self.k = paramaters["k"]    

    def check_ooc(self,stat: float) -> bool:
        pass
    
    def ub_lb(self) -> np.array:
        pass

#HWMA SCHEME   
class HWMA(SPM_uni_chart):
    def chart_stat(self,series) -> float:
        return self.phi*series[-1] + (1-self.phi)*np.mean(series[:-1])
    
    def chart_var(self,t) -> float:
        if t==1:
            return (self.phi**2)*(self.sig2)
        else:
            return ((self.phi**2) + (((1-self.phi)**2)/(t-1)))*(self.sig2)

#Extended HWMA SCHEME    
class EHWMA(SPM_uni_chart):
    def chart_stat(self,series) -> float:
        pass

    def chart_var(self,t) -> float:   
        pass
    
#EWMA SCHEME    
class EWMA(SPM_uni_chart):
    def chart_stat(self,series) -> float:
        pass

    def chart_var(self,t) -> float:   
        pass 
  
#Extended EWMA SCHEME    
class EEWMA(SPM_uni_chart):
    def chart_stat(self,series) -> float:
        pass

    def chart_var(self,t) -> float:   
        pass  
    
#Modified EWMA SCHEME    
class MEWMA(SPM_uni_chart):
    def chart_stat(self,series) -> float:
        pass

    def chart_var(self,t) -> float:   
        pass
    
    
    
       
#class (SPM_uni_chart):
#    def chart_stat(self,series) -> float:

    
 #   def chart_var(self,t) -> float:
