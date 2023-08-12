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
# Hay muchas formas de implementar esto realmente, podría en la función principal calcular la media y según put_or_call poner K = S o S = mean y luego usar payOff. Pero bueno, está bien 
def asianPayOff(S,K, mean, put_or_call):
  if (put_or_call == 'PC'):
    return max(mean-K, 0) 
  if (put_or_call == 'PP'):
    return max(K-mean, 0) 
  if (put_or_call == 'SC'):
    return max(S-mean, 0)
  if (put_or_call == 'SP'):
    return max(mean-S, 0)

