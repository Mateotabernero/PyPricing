import numpy as np 
import math 
import scipy.stats as stats
from BlackScholes import * 


class BlackScholesOption:
    def  __init__ (self, spot_price, strike_price, maturity, call_or_put, risk_free_rate, volatility, div= 0):
        self.S     = spot_price
        self.K     = strike_price
        self.T     = maturity 
        self.CoP   = call_or_put
        self.r     = risk_free_rate
        self.sigma = volatility 
        self.div   = div
 
    def _d1(self): 
        d1 = calc_d_1(self.K, self.S, self.r, self.T, self.sigma, div = self.div)
        return d1 
       
    def _d2(self): 
        d2 = calc_d_2(self.K, self.S, self.r, self.T, self.sigma, div = self.div)
        return d2 

    def price(self): 
        d1 = self._d1() 
        d2 = self._d2() 
        option_price = BSprice (self.K, self.S, self.r, self.T, self.sigma, self.CoP, div = self.div)
        
        return option_price 
    
    def delta(self):
        d1 = self._d1() 
        if self.CoP == 'C':
            delta = stats.norm.cdf(d1) 
        elif self.CoP == 'P':
            delta = -stats.norm.cdf(-d1) 
        return delta 

    def gamma(self): 
        gamma_ = gamma(self.K, self.S, self.r, self.T, self.sigma, self.CoP, div = self.div)
        return gamma_ 
    
    def vega(self): 
        vega_ = vega(self.K, self.S, self.r, self.T, self.sigma, self.CoP, div = self.div)
        return vega_
    
    def theta(self):

        theta_ = theta(self.K, self.S, self.r, self.T, self.sigma, self.CoP, div = self.div) 
        return -theta_ 

    def rho(self): 
        rho_    = rho(self.K, self.S, self.r, self.T, self.sigma, self.CoP, div = self.div) 
        return rho_
