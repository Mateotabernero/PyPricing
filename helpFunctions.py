### THIS FILE INCLUDES SEVERAL FUNCTIONS THAT WILL BE HELPFUL IN THE OTHER ONES ###

# A function to calculate the (vanilla) payOff of a function
def payOff (S,K, put_or_call):
    """
    Calculate the payoff of an American or European option at some moment

    : param S            : Current price of the underlying stock
    : param K            : Exercise price 
    : param put_or_call  : Is the option a put ('P') or a call ('C')?
    : return             : payoff of the option 
    """
    if (put_or_call == 'C'): 
        return max(S-K,0) 
    elif (put_or_call == 'P'):
        return max (K-S, 0) 
    else: 
        raise ValueError ("Please choose a valid value for put_or_call: Put ('P') or Call ('C')") 
        
def asianPayOff(S,K, mean, put_or_call):
    """
    Calculate the payoff of an Asian option 
    
    : param S           : Current price of the underlying stock 
    : param K           : Exercise price 
    : mean              : Mean of the stock prices during the lifetime of the option 
    : put_or_call       : Type of Asian option: price call ('PC'), price put ('PP'), strike call ('SC') or strike put ('SP')
    : return            : payoff of the option
    """
  if (put_or_call == 'PC'):
    return max(mean-K, 0) 
  if (put_or_call == 'PP'):
    return max(K-mean, 0) 
  if (put_or_call == 'SC'):
    return max(S-mean, 0)
  if (put_or_call == 'SP'):
    return max(mean-S, 0)
  else: 
    raise ValueError ("Please choose a valid value for put_or_call: Price Call ('PC')', Price Put ('PP'), Strike Call ('SC') or Strike Put ('SP')")

def mu_sigma(prices):
    """
    Calculate the log returns from a series of prices and then compute the mean (as an approximation of the drift) and the std (as an approximation of the volatility) 

    : param prices       : An array with the prices of the daily prices of a stock 
    : return             : A pair containing the mean of the log returns and the standard deviation 
    """
  log_returns = np.zeros(len(log_prices)-1)
  for i in range(len(log_returns)):
    log_returns[i] = math.log(prices[i+1]/prices[i])
  mu = np.mean(log_returns)
  sigma = np.std(returns) 
  return (mu, sigma) 
