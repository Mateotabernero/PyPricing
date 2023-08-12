### THIS FILE INCLUDES SEVERAL FUNCTIONS THAT WILL BE HELPFUL IN THE OTHER ONES ###





# This function calculates the log returns from a series of prices and then compute the mean (as an approximation of mu) and the std (as an approximation of sigma)
def mu_sigma(prices):
  log_returns = np.zeros(len(log_prices)-1)
  for i in range(len(log_returns)):
    log_returns[i] = math.log(prices[i+1]/prices[i])
  mu = np.mean(log_returns)
  sigma = np.std(returns) 
  return (mu, sigma) 

# A function to calculate the (vanilla) payOff of a function
def payOff (S,K, put_or_call): 
    if (put_or_call == 'C'): 
        return max(S-K,0) 
    elif (put_or_call == 'P'):
        return max (K-S, 0) 


