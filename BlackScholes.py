import numpy as np 
import math 
import scipy.stats as stats

def calc_d_1(K, S, r, T, sigma, t, delta = 0):
    d_1 = (math.log(S/K) + (r-delta+sigma**2/2)*(T-t))/(sigma*math.sqrt(T-t))
    return d_1
def calc_d_2(K, S, r, T, sigma, t, delta = 0):
  d_2 = (math.log(S/K) + (r-delta-sigma**2/2)*(T-t))/(sigma*math.sqrt(T-t))
  return d_2
def eu_BS (K,S,r, T, sigma, t, call_or_put, delta = 0):
    d_1 = calc_d_1(K, S, r, T, sigma, t, delta = delta) 
    d_2 = calc_d_2(K, S, r, T, sigma, t, delta = delta) 
    if (call_or_put == 'C'):
        V = S*math.exp(-delta*(T-t))*stats.norm.cdf(d_1)-K*math.exp(-r*(T-t))*stats.norm.cdf(d_2) 
    elif (call_or_put == 'P'):
        V = -S*math.exp(-delta*(T-t))*stats.norm.cdf(d_1)+K*math.exp(-r*(T-t))*stats.norm.cdf(d_2)
    
    return V 
def delta(K, S, r,T, sigma, t, call_or_put, delta = 0):
    """
    Calculate the delta of an european option (Black-Scholes model) 

    : param K      : Strike price of the option 
    : S            : Price of the underlying stock 
    : r            : Risk-free interest rate 
    : T            : Expiration time
    : sigma        : Volatility
    : t            : Time 
    : call_or_put  : Type of option: Call ('C') or Put ('P') 
    : delta        : Dividends 
    : returns      : delta of the option 
    """
    d_1 = calc_d_1(K, S, r, T, sigma, t, delta = delta)
    if (call_or_put == 'C'):
        return math.exp(-delta*(T-t))*stats.norm.cdf(d_1)
    else:
        return -math.exp(-delta*(T-t))*stats.norm.cdf(-d_1) 


def vega(K, S, r, T, sigma, t, call_or_put, delta = 0):
    """
    Calculate the vega of an european option (Black-Scholes model) 

    : param K      : Strike price of the option 
    : S            : Price of the underlying stock 
    : r            : Risk-free interest rate 
    : T            : Expiration time
    : sigma        : Volatility
    : t            : Time 
    : call_or_put  : Type of option: Call ('C') or Put ('P') 
    : delta        : Dividends 
    : returns      : vega of the option 
    """
    d_1 = calc_d_1(K, S, r, T, sigma, t, delta = delta)

    return S*math.exp(-delta*(T-t))*stats.norm.pdf(d_1)*math.sqrt(T-t)


def theta(K, S, r, T, sigma, t, call_or_put, delta = 0):
    """
    Calculate the theta of an european option (Black-Scholes model) 
    
    : param K      : Strike price of the option 
    : S            : Price of the underlying stock 
    : r            : Risk-free interest rate 
    : T            : Expiration time  
    : sigma        : Volatility
    : t            : Time 
    : call_or_put  : Type of option: Call ('C') or Put ('P') 
    : delta        : Dividends 
    : returns      : theta of the option 
    """
    d_1 = calc_d_1(K, S, r, T, sigma, t, delta = delta)
    d_2 = calc_d_2(K, S, r, T, sigma, t, delta = delta) 
    # Obviamente esta función puede mejorar mucho,y lo hará 
    term_1 = -math.exp(-delta*(T-t))*S*stats.norm.pdf(d_1)*sigma/(2*(T-t))
    if (call_or_put == 'C'):
        term_2 = -r*K*math.exp(-r*(T-t))*stats.norm.cdf(d_2) 
        term_3 = delta*S*math.exp(-delta*(T-t))*stats.norm.cdf(d_1)
    elif (call_or_put == 'P'):
        term_2 = r*K*math.exp(-r*(T-t))*stats.norm.cdf(-d_2) 
        term_3 = -delta*S*math.exp(-delta*(T-t))*stats.norm.cdf(d_1)
    else: 
        raise ValueError("Please choose an appropiate value")
    return (term_1 + term_2 + term_3)

def gamma(K, S, r, T, sigma, t, call_or_put, delta = 0):
    """
    Calculate the gamma of an european option (Black-Scholes model) 
    
    : param K      : Strike price of the option 
    : S            : Price of the underlying stock 
    : r            : Risk-free interest rate 
    : T            : Expiration time  
    : sigma        : Volatility
    : t            : Time 
    : call_or_put  : Type of option: Call ('C') or Put ('P') 
    : delta        : Dividends 
    : returns      : gamma of the option 
    """
    d_1 = calc_d_1(K, S, r, T, sigma, t, delta = delta) 
    return math.exp(-delta*(T-t))*stats.norm.cdf(d_1)/(S*sigma*math.sqrt(T-t)) 

def rho(K, S, r, T, sigma, t, call_or_put, delta = 0): 
    """
    Calculate the rho of an european option (Black-Scholes model) 
    
    : param K      : Strike price of the option 
    : S            : Price of the underlying stock 
    : r            : Risk-free interest rate 
    : T            : Expiration time  
    : sigma        : Volatility
    : t            : Time 
    : call_or_put  : Type of option: Call ('C') or Put ('P') 
    : delta        : Dividends 
    : returns      : rho of the option 
    """
    d_2 = calc_d_2(K, S, r, T, sigma, t, delta = delta) 
    if (call_or_put == 'C'): 
        return K* (T-t)*math.exp(-r*(T-t)) * stats.math.cdf(d_2) 
