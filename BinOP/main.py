import numpy as np 
import math 
import scipy.stats as stats 
import BinOp

class BinOption: 
    def __init__(self, spot_price, strike_price, maturity, option_type, call_or_put, risk_free_rate, volatility, M, gamma_par = 1): 
        self.S         = spot_price
        self.K         = strike_price
        self.T         = maturity 
        self.CoP       = call_or_put
        self.r         = risk_free_rate
        self.sigma     = volatility 
        self.gamma_par = gamma_par
        self.OT        = option_type
        self.M         = M 

        self.values, self.prices = BinOp.generate_tree(self.r, self.sigma, self.S, self.T, self.K, self.CoP, self.OT, self.M, gamma_par = self.gamma_par)

    def value(self): 
        return self.values[0][0]



    # Functiona bastante mejor de lo esperado
    
    def delta(self): 
        return (self.values[1][1] - self.values[1][0])/(self.prices[1][1] - self.prices[1][0])
    
    def theta(self): 
        return -(self.values[2][1] - self.values[0][0]) / (2*(self.T/self.M))
    
    def vega(self):
        new_sigma = 1.01*self.sigma
        new_values, new_prices = BinOP.generate_tree(self.r, new_sigma, self.S, self.T, self.K, self.CoP, self.OT, self.M, gamma_par = self.gamma_par)

        return (new_values[0][0] - self.values[0][0])/(new_sigma - self.sigma) 
     
    
     
