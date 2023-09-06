import GBM 
import heston 
import payOffs
import numpy as np 

EuPayOff = payOffs.EuPayOff 
AsPayOff = payOffs.AsPayOff 

class MCGBMOption: 
    def __init__(self, risk_free_rate, volatility, spot_price, strike_price, maturity, call_or_put, payOff = EuPayOff): 
        """ 
        Initialize the option 
        
        : param risk_free_rate : risk free rate 
        : param volatility     : Volatility 
        : param spot_price     : Spot price of the option 
        : param strike_price   : Strike price of the option 
        : param maturity       : Maturity of the option 
        : param call_or_put    : The option being a call or a put. The possibilities vary depending on the type of options. They are the same as in the payOff functions 
        : param payOff         : The payOff of the option. Some predefined payoff functions are EuPayOff (European options), AsPayOff (Asian options) (Default value: EuPayOf) 
        
        """

        
        self.S   = spot_price 
        self.K   = strike_price 
        self.T   = maturity 
        self.r   = risk_free_rate
        self.sig = volatility 
        
        self.payOff     = payOff
        self.CoP        = call_or_put


    def generate_paths(self, num_steps, num_simulations = 10**4, integration_method = 'E', ant_variates = False):
        S = GBM.GBM(self.r, self.sig, self.S, num_steps, self.T, num_simulations, integration_method, ant_variates)
     
        return S 
    

    def price(self, num_steps, num_simulations = 10**4, integration_method = 'E', ant_variates = False): 



        S =  self.generate_paths(num_steps, num_simulations = num_simulations, integration_method = integration_method, ant_variates = ant_variates)
        
        return np.exp(-self.r*self.T)*(np.mean(self.payOff(S, self.K, self.CoP))) 

    def delta(self, num_steps, num_simulations = 10**4, integration_method = 'E', ant_variates = False):
        new_S0 = self.S*1.01

        price = self.price(num_steps, num_simulations, integration_method, ant_variates) 

        new_S = GBM.GBM(self.r, self.sig, new_S0, num_steps, self.T, num_simulations, integration_method, ant_variates)
        new_price = np.exp(-self.r*self.T)*(np.mean(self.payOff(new_S, self.K, self.CoP)))
         
        return (new_price - price)/(new_S0 - self.S) 

    def vega(self, num_steps, num_simulations = 10**4, integration_method = 'E', ant_variates = False): 
        new_sig = self.sig*1.01
        price = self.price(num_steps, num_simulations, integration_method, ant_variates) 

        new_S = GBM.GBM(self.r, new_sig, self.S, num_steps, self.T, num_simulations, integration_method, ant_variates)
        new_price = np.exp(-self.r*self.T)*(np.mean(self.payOff(new_S, self.K, self.CoP)))

        return -(new_price - price)/(new_sig- self.sig) 
    
    def theta(self, num_steps, num_simulations = 10**4, integration_method = 'E', ant_variates = False): 
        # Still need to define the function 
        pass 
        
class MCHestonOption: 
    def __init__(self,  risk_free_rate, volatility_0, spot_price, strike_price, maturity, kappa, theta, xi,call_or_put, payOff = EuPayOff): 
        self.S     = spot_price
        self.K     = strike_price 
        self.T     = maturity 
        self.r     = risk_free_rate
        self.v_0    = volatility_0
        self.kappa = kappa 
        self.theta = theta 
        self.xi    = xi 
        self.payOff = payOff
        self.CoP   = call_or_put

    def generate_paths(self, num_steps, num_simulations = 10**4, corr_index = 0): 
        S, v = heston.heston(self.r, self.v_0, self.S, self.theta, self.xi, num_steps, corr_index = corr_index, num_simulations = num_simulations) 
        return S, v

    def price(self, num_steps, num_simulations = 10**4, corr_index = 0): 

        S, v = self.generate_paths(num_steps, num_simulations = num_simulations, corr_index= corr_index)
        
        return np.exp(-self.r*self.T)*(np.mean(self.payOff(S, self.K, self.CoP)))
    
    def delta(self, num_steps, num_simulations = 10**4, corr_index = 0): 
        new_S0 = self.S*1.01
        
        price = self.price(num_steps, num_simulations, corr_index) 

        new_S, new_v = heston.heston(self.r, self.v_0, new_S0, self.theta, self.xi, num_steps, corr_index, num_simulations) 
        
        new_price = np.exp(-self.r*self.T)*np.mean(self.payOff(new_S, self.K, self.CoP)) 

        return (new_price - price)/(new_S0 - self.S) 
    


