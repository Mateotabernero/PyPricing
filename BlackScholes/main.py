import numpy as np 
import scipy.stats as stats
from BlackScholes import * 


class BlackScholesOption:
    def  __init__ (self, risk_free_rate, volatility, spot_price, strike_price, maturity, call_or_put, div= 0):
        
        self.r     = risk_free_rate
        self.sigma = volatility 
        self.S     = spot_price
        self.K     = strike_price
        self.T     = maturity 
        self.CoP   = call_or_put
        self.div   = div
 
    def _d1(self): 
        """
        Calculate d1 in the Black-Scholes model
        : return : d1 
        """
        d1 = calc_d_1(self.r, self.sigma, self.S, self.K, self.T, div = self.div)
        return d1 
       
    def _d2(self): 
        """
        Calculate d2 in the Black-Scholes model 
        : return : d2 
        """
        d2 = calc_d_2(self.r, self.sigma, self.S, self.K, self.T, div = self.div)
        return d2 

    def value(self): 
        """
        Calculate the option value
        : return : Value of the option 
        """
        d1 = self._d1() 
        d2 = self._d2() 
        option_price = BSprice (self.r, self.sigma, self.S, self.K, self.T, self.CoP, div = self.div)
        
        return option_price 
    
    def delta(self):
        """
        Calculates the delta of the option
        : returns : Delta 
        """
        d1 = self._d1() 
        if self.CoP == 'C':
            delta = stats.norm.cdf(d1) 
        elif self.CoP == 'P':
            delta = -stats.norm.cdf(-d1) 
        return delta 

    def gamma(self): 
        """
        Calculates the gamma of the option 
        : returns : Gamma 
        """
        gamma_ = gamma(self.r, self.sigma, self.S, self.K, self.T, self.CoP, div = self.div)
        return gamma_ 
    
    def vega(self): 
        """ 
        Calculates the vega of the option 
        : return : Vega 
        """
        vega_ = vega(self.r, self.sigma, self.S, self.K, self.T, self.CoP, div = self.div)
        return vega_
    
    def theta(self):
        """
        Calculates the theta of the option 
        : return : Theta 
        """
        theta_ = theta(self.r, self.sigma, self.S, self.K, self.T, self.CoP, div = self.div) 
        return -theta_ 

    def rho(self):
        """
        Calculates the rho of the option 
        : return : rho 
        """
        rho_    = rho(self.r, self.sigma, self.S, self.K, self.T, self.CoP, div = self.div) 
        return rho_
