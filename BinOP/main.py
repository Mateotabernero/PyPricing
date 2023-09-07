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

        self.values, self.prices = BinOp.generate_tree(self.r, self.sigma, self.S, self.K, self.T, self.CoP, self.OT, self.M, gamma_par = self.gamma_par)

    def value(self): 
        """
        Get the value of the option 
        : return : The value of the option
        """
        return self.values[0][0]

    def delta(self):
        """
        Calculates the delta of the option
        : return : Delta of the option
        """
        return (self.values[1][1] - self.values[1][0])/(self.prices[1][1] - self.prices[1][0])
    
    def theta(self):  
        """
        Calculates the theta of the option
        : return : Theta of the option
        """
        return -(self.values[2][1] - self.values[0][0]) / (2*(self.T/self.M))
    
    def vega(self):
        """
        Calculates the vega of the option 
        : return : Vega of the option
        """
        new_sigma = 1.01*self.sigma
        new_values, new_prices = BinOP.generate_tree(self.r, new_sigma, self.S, self.T, self.K, self.CoP, self.OT, self.M, gamma_par = self.gamma_par)

        return (new_values[0][0] - self.values[0][0])/(new_sigma - self.sigma) 
     
    def rho(self): 
        """
        Calculates the rho of the option
        : return : Rho of the option 
        """
        new_r = 1.01*self.r
        new_values, new_prices = BinOp.generate_tree(new_r, self.sigma, self.S, self.T, self.K, self.CoP, self.OT, self.M, gamma_par = self.gamma_par) 

        return (new_values[0][0] - self.values[0][0])/(new_r - r) 
     
