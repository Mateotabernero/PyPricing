import numpy as np

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
