import numpy as np

def heston(r, sigma_0, S_0, kappa, theta, xi, num_steps, T, corr_index = 0, num_simulations = 10000): 
    delta_t = T/num_steps

    S = np.zeros((num_simulations, num_steps +1))
    v = np.zeros((num_simulations, num_steps +1))
    W = np.sqrt(delta_t)*np.random.normal(0,1,(2,num_simulations, num_steps))
    W[1,:] = corr_index*W[0,:] + np.sqrt(1-corr_index**2)*W[1,:]

    S[:,0] = S_0
    v[:,0] = sigma_0**2 

    for j in range(num_steps): 
        S[:,j+1] = r*S[:,j]*delta_t + np.sqrt(v[:,j])*S[:,j]*W[0,:,j]
        v[:,j+1] = kappa*(theta - v[:,j])*delta_t + xi*np.sqrt(v[:,j])*W[1,:,j]
    
    return (S,v)