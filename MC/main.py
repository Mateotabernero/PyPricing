import GBM 
import heston 

class MCGBMOption: 
    def __init__(self, spot_price, strike_price, maturity, call_or_put, risk_free_rate, volatility, payOff = GBM.EuPayoff, *args): 
        self.S   = spot_price 
        self.K   = strike_price 
        self.T   = maturity 
        self.r   = risk_free_rate
        self.sig = volatility 
        
        self.payOff     = payOff
        self.optionType = option_type
        self.CoP        = call_or_put

    # Aquí definiría las payOffs según el tipo de opción con la que estemos tratando y la definiría como un atributo de clase


    def generate_paths(self, num_steps, num_simulations = 10**4, integration_method = 'E', ant_variates = False):
        S = GBM.GBM(self.r, self.sig, self.S, num_steps, self.T, num_simulations, integration_method, ant_variates)
     
        return S 
    

    def price(self, num_steps, num_simulations = 10**4, integration_method = 'E', ant_variates = False): 

        # Aquí creo que da un poco igual si cogemos self.generate_paths o la función original GBM.GBM. Si al ginal son iguales 
        # Esta igual mejor porque no hay que meter tantos argumentos (como r, sigma, o T) 

        S =  self.generate_paths(num_steps, num_simulations = num_simulations, integration_method = integration_method, ant_variates = ant_variates)
        
        return np.exp(-self.r*self.T)*(np.mean(self.payOff(S, self.K, *args))) 

    def delta(self, num_steps, num_simulations = 10**4, integration_method = 'E', ant_variates = False):
        new_S = self.S*1.01

        price = self.price(num_steps, num_simulations, integration_method, ant_variates) 

        new_S = GBM.GBM(self.r, self.sig, new_S, num_steps, self.T, num_simulations, integration_method, ant_variates)
        new_price = np.exp(-self.r*self.T)*(np.mean(self.payOff(new_S, self.K, *args)))
         
        return (new_price - price)/(new_S - self.S) 

    def vega(self, num_steps, num_simulations = 10**4, integration_method = 'E', ant_variates = False): 
        new_sig = self.sig*1.01

        price = self.price(num_steps, num_simulations, integration_method, ant_variates) 

        new_S = GBM.GBM(self.r, new_sig, self.S, num_steps, self.T, num_simulations, integration_method, ant_variates)
        new_price = np.exp(-self.r*self.T)*(np.mean(self.payOff(new_S, self.K, *args)))

        return (new_price - price)/(new_S - self.S) 
    
    def theta(self, num_steps, num_simulations = 10**4, integration_method = 'E', ant_variates = False): 
        # Still need to define the function 
        pass 
        
class MCHestonOption: 
    def __init__(self, spot_price, strike_price, maturity, risk_free_rate, volatility_0, kappa, theta, xi): 
        self.S     = spot_price
        self.K     = strike_price 
        self.T     = maturity 
        self.r     = risk_free_rate
        self.v_0    = volatility_0
        self.kappa = kappa 
        self.theta = theta 
        self.xi    = xi 

    def generate_paths(self, num_steps, num_simulations = 10**4, corr_index = 0): 
        S, v = heston.heston(self.r, self.v_0, self.S, self.theta, self.xi, num_steps, corr_index = corr_index, num_simulations = num_simulations) 
        return S, v

    def price(self, num_steps, num_simulations = 10**4, corr_index = 0): 

        S, v = self.generate_paths(num_steps, num_simulations = num_simulations, corr_index= corr_index)
        
        return np.exp(-self.r*self.T)*(np.mean(self.payOff(S, self.K, *args)))
    
    def delta(self, num_steps, num_simulations = 10**4, corr_index = 0): 
        new_S = self.S*1.01
        
        price = self.price(num_steps, num_simulations, corr_index) 

        new_S, new_v = heston.heston(self.r, self.v_0, new_S, self.theta, self.xi, num_steps, corr_index, num_simulations) 
        
        new_price = np.exp(-self.r*self.T)*np.mean(self.payOff(new_S, self.K, *args)) 

        return (new_price - price)/(new_S - self.S) 
    
