import numpy as np
import PayOffs 


def heston(r, sigma_0, S_0, kappa, theta, xi, num_steps, T, corr_index = 0, num_simulations = 10000): 
    """
    Calculate sample paths of Heston model 

    : param r                  : The drift 
    : param sigma_0            : The initial volatility 
    : param S_0                : The initial price 
    : param kappa              : Kappa parameter in Heston model 
    : param theta              : Theta parameter in Heston model 
    : param xi                 ; Xi parameter in Heston model 
    : param num_steps          : Number of steps for the random path generation  
    : param T                  : Time length of the generated path 
    : param corr_index         : Correlation index between the interest rate Wiener process and the volatility Wiener process
    : param num_simulations    : The number of paths generated (default value: 10000)  
    : returns                  : A numpy array containing the generated paths of both the prices and the volatility     
    
    """

    delta_t = T/num_steps

    S = np.zeros((num_simulations, num_steps +1))
    v = np.zeros((num_simulations, num_steps +1))
    W = np.sqrt(delta_t)*np.random.normal(0,1,(2,num_simulations, num_steps))
    W[1,:] = corr_index*W[0,:] + np.sqrt(1-corr_index**2)*W[1,:]

    S[:,0] = S_0
    v[:,0] = v_0

    for j in range(num_steps): 
        S[:,j+1] = S[:,j] + r*S[:,j]*delta_t + np.sqrt(np.maximum(v[:,j],0))*S[:,j]*W[0,:,j]
        v[:,j+1] = v[:,j] + kappa*(theta - v[:,j])*delta_t + xi*np.sqrt(np.maximum(v[:,j],0))*W[1,:,j]
    
    return (S,v)


def eu_heston(r, sigma_0, S_0, K, kappa, theta, xi, num_steps, T, call_or_put, corr_index, num_simulations = 10000): 
    """
    Computes the value of an European option under GBM using Monte Carlo method 

    : param r                   : Risk-free interest rate 
    : param sigma_0             : The initial volatility 
    : param S_0                 : Spot price
    : param K                   : Strike price 
    : param kappa               : Kappa parameter in Heston model 
    : param theta               : Theta parameter in Heston model 
    : param xi                  : Xi parameter in Heston model 
    : param num_steps           : Number of steps on the generation of paths
    : param T                   : Maturity 
    : param call_or_put         : Whether the option is a call ('C') or a put ('P')
    : param corr_index          : Correlation index between the two Wiener processes (default value: 0)  
    : param num_simulations     : Number of paths generated for MC (default value: 10000) 
    : returns                   : Value of the option 

    """
    
    S, v = heston(r, sigma_0, S_0, kappa, theta, xi, num_steps, T, corr_index = corr_index, num_simulations = num_simulations)
    Vs   = payOffs.EuPayOff(S, K, call_or_put)
    V    = np.exp(-r*T)*np.mean(Vs) 
    return V 

def am_heston(r, sigma_0, S_0, K, kappa, theta, xi, num_steps, T, call_or_put, corr_index, num_simulations = 10000):
    
    """
    Computes the value of an European option under GBM using Monte Carlo method 

    : param r                   : Risk-free interest rate 
    : param sigma_0             : The initial Volatility 
    : param S_0                 : Spot price
    : param K                   : Strike price 
    : param kappa               : Kappa parameter in Heston model 
    : param theta               : Theta parameter in Heston model 
    : param xi                  : Xi parameter in Heston model 
    : param num_steps           : Number of steps on the generation of paths
    : param T                   : Maturity 
    : param call_or_put         : Whether the option is a Price call ('PC'), a Price put ('PP'), a strike call ('SC') or a strike put ('SP') 
    : param corr_index          : Correlation index between the two Wiener processes (default value: 0)  
    : param num_simulations     : Number of paths generated for MC (default value: 10000) 
    : returns                   : Value of the option 

    """
    
    S, v = heston(r, sigma_0, S_0, kappa, theta, xi, num_steps, T, corr_index = corr_index, num_simulations = num_simulations)
    Vs   = payOffs.AmPayOff(S, K, call_or_put)
    V    = np.exp(-r*T)*np.mean(Vs) 
    return V 
