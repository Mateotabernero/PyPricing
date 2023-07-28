import numpy as np 
import yfinance 
import matplotlib.pyplot as plt 
import math 
import pandas as pd 


# This function calculates the log returns from a series of prices and thus compute the mean (as an approximation of mu) and the std (as an approximation of sigma)
def mu_sigma(prices):
  log_returns = np.zeros(len(log_prices)-1)
  for i in range(len(log_returns)):
    log_returns[i] = math.log(prices[i+1]/prices[i])
  mu = np.mean(log_returns)
  sigma = np.std(returns) 
  return (mu, sigma) 


#This function calculates GBM trajectories, steps is the number of steps and T the total time 
def gbm_trajectories(mu, sigma, T, steps, initial_value, num_trajectories = 10000):
  delta_t = T /steps
  S = np.zeros(num_trajectories, steps +1)   
  W = np.random.normal(0,1) 
  for i in range(num_trajectories):
    S[i,0] = initial_value 
  for i in range(num_trajectories);
    for j in range(time);
      S[i, j+1] = S[i,j] + mu*S[i,j] +sigma*S[i,j]*(math.sqrt(delta_t)*W[i,j])
  return S 

# Calculation of GBM trajectories using antithetic variates 

def gbm_ant_trajectories(mu, sigma, T, steps, initial_value, num_trajectories = 10000):
  delta_t = T /steps  
  S = np.zeros((num_trajectories, steps+1))
  ant_S = np.zeros((num_trajectories, steps+1))
  W = np.random.normal(0,1, (num_trajectories, steps+1))
  for i in range(num_trajectories): 
      S[i,0] = initial_value
      ant_S[i,0] = initial_value 
  for i in range(num_trajectories):
      for j in range(time):
          S[i][j+1] = S[i][j] + mu*S[i][j] + sigma*S[i][j] *(math.sqrt(delta_t) W[i][j])
          ant_S[i][j+1] = ant_S[i][j] + mu*ant_S[i][j] +sigma*ant_S[i][j] * (-math.sqrt(delta_t)*W[i][j])
    
  combined_S = np.concatenate((S, ant_S), axis = 0) 
  return combined_S 


# This is an improved version of the trajectories function. It allows to choose between three different SDE integration methods and if using antithetic variates or not
def GBM(r, sigma, S_0, num_steps, T, num_simulations = 10000, integration_method = 'E', ant_variates = False):
    delta_t = T/num_steps 

    S = np.zeros((num_simulations, num_steps +1))
    W = np.random.normal(0,1,(num_simulations, num_steps)) 

    if ant_variates: 
        ant_S = S 

    for i in range(num_simulations):
        S[i,0] = S_0 
    
    for i in range(num_simulations):
        for j in range(num_steps): 
            # This values are common to the three methods of integration 

            deterministic_term = r*S[i,j]*delta_t
            random_term = sigma*S[i,j]*(math.sqrt(delta_t)*W[i,j])

            if ant_variates :
                ant_deterministic_term = r*ant_S[i,j]*delta_t 
                ant_random_term  = sigma*ant_S[i,j]*(-math.sqrt(delta_t)*W[i,j]) 
            
            if integration_method == 'E': 
                S[i,j+1] = S[i,j] + deterministic_term + random_term
                
                if ant_variates:
                    ant_S[i,j+1] = ant_S[i,j] + ant_deterministic_term + ant_random_term
            
            elif integration_method == 'M':
                milstein_term = 1/2 * (sigma**2)*S[i,j]*((math.sqrt(delta_t)*W[i,j])**2 - delta_t)
                S[i,j+1] = S[i,j] + deterministic_term + random_term + milstein_term
                
                if ant_variates:
                    ant_milstein_term = 1/2 * (sigma**2)*ant_S[i,j]*((-math.sqrt(delta_t)*W[i,j])**2 - delta_t)
                    ant_S[i,j+1] = ant_S[i,j] + ant_deterministic_term + ant_random_term + ant_milstein_term
        
            elif integration_method == 'RK': 
                y_hat = S[i,j] + r*S[i,j]*delta_t + sigma*math.sqrt(delta_t) 
                rk_term = ((math.sqrt(delta_t)*W[i,j])**2 - delta_t) * sigma*(y_hat - S[i,j]) /(2*math.sqrt(delta_t))
                S[i, j+1] = S[i,j] + deterministic_term + random_term + rk_term 

                if ant_variates:
                    ant_y_hat =  ant_S[i,j] + r*ant_S[i,j]*delta_t + sigma*math.sqrt(delta_t)
                    ant_rk_term =((-math.sqrt(delta_t)*W[i,j])**2 - delta_t) * sigma*(ant_y_hat - ant_S[i,j]) /(2*math.sqrt(delta_t))
                    ant_S[i,j+1] = ant_S[i,j] + ant_deterministic_term + ant_random_term + ant_rk_term
            
            else: 
                raise ValueError ("Please choose an appropiate SDE integration method (Euler ('E'), Milstein ('M') or Rude-Kutta ('RK'))")
    
    if ant_variates:
        return (S, ant_S)
    
    return S


# Here's the payoff. I will put it in a separate file so that functions from different files can access it:
def payOff (S,K, put_or_call, bound = 0): 
    if (put_or_call == 'C'): 
        return max(S-K,bound) 
    elif (put_or_call == 'P'):
        return max (K-S, bound) 
# Then we can value european options with GBM using the following algorithm:

def eu_GBM(r, sigma, S_0, K, num_steps, T, put_or_call, num_simulations = 10000, integration_method = 'E', ant_variates = False): 
    S = GBM(r, sigma, S_0, num_steps, T, num_simulations = num_simulations, integration_method = 'E', ant_variates = False)
    Vs = np.vectorize(payOff) (S[:, num_steps], K, put_or_call)
    V = math.exp(-r*T)*np.mean(Vs) 
    return V 

# Similarly, once we define the cir_GBM function we have a function that uses Montecarlo to value options under GBM + CIR stock price evolution 

def eu_cir_GBM (r_0, sigma, S_0, K, R, sigma_r, num_steps, T, put_or_call, num_simulations = 10000, integration = 'E', ant_variates = False):

    # Esta función la tengo definida en el portátil 
    # Puedo incluso definir dos parámetros de integration type y de variates, uno para S y otro para r. Sería lo mejor aunque más trabajo

    (S,r) = cir_GBM(r_0, sigma, S_0, sigma_r, num_steps,T, integration = 'E', ant_variates = False) 
    
    # Lo que viene ahora se puede hacer mejor vectorizando np.mean o algo así seguro 
    average_r = np.zeros(num_simulations)
    for i in range(num_simulations):
        average_r[i] = np.mean(r[i, :])
    Vs = np.zeros (num_simulations)  
    for i in range(i):
        #esto creo que es correcto, cogemos la media de las r para cada valor y luego tomamos medias.
        Vs[i] = math.exp(-r[i]*T) *payOff(S[i, num_steps], K, put_or_call) 
    V = np.mean(Vs) 
    return V 


# AQUÍ PARA VALORAR OPCIONES AMERICANAS CON LA APROXIMACIÓN DE HORIZONTAL STOPPING TIMES UNDER GBM EVOLUTION. cogo el modelo en el que si en ninguno se hitea beta, se coge el último momento (parece lógico) 

# Esta función, dada la evolución de precios y beta calcula los stopping time
def stopping_times (prices, beta):
    condition_array = prices > beta 
    (x,y) = prices.shape 
    stopping_times = np.zeros(x) 
    for i in range(x):
        first_index = int(np.argmax(condition_array[i]))
        if condition_array[i, first_index]:
            stopping_times[i] = int(first_index)
        else: 
            stopping_times[i] = int(y-1)  
    
    return stopping_times.astype(int) 
# now given the stopping times the prices and the option information (r, K, put_or_call), calcula el valor 

def value (prices, r, stopping_times, K, put_or_call):
  (x,y) = prices.shape 
  payOffs = np.zeros(x) 
  for i in range(x):
    payOffs[i] = math.exp(-r*stopping_times[i])*payOff(prices[i, stopping_times[i]], K, put_or_call) 
  mean_payOff = np.mean(payOffs) 
  return mean_payOff

# Y ya juntamos todo en un único algoritmo que ya lo hace todo 
def am_GBM (S_0, r, sigma, K, put_or_call, T, num_steps):
  S = GBM (r, sigma, S_=, num_steps, T)
  betas = [K + 0.1*i*K for i in range(1,20)]
  betas_values = np.zeros(19) 
  for i in range (19):
    betas_values[i] = value(S, 0, stopping_times(S, betas[i]), K, put_or_call)  
# Y aquí betas_values son básicamente las aproximaciones que hay para el valor. Se cogería el máximo y a correr
  return np.max(betas_values[i]) 
