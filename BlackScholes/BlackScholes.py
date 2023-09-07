import numpy as np 

import scipy.stats as stats

def calc_d_1(r, sigma, S, K, T, div = 0):
    """
    Calculate the value d1 in Black-Scholes model

    : param K           : Strike price of the option 
    : param S           : Spot price of the underlying stock 
    : param r           : Risk-free interest rate 
    : param T           : Time for maturity  
    : param sigma       : Volatility 
    : param div         : Dividends 
    : returns           : d1
    """
    d_1 = (np.log(S/K) + (r-div+sigma**2/2)*(T))/(sigma*np.sqrt(T))
    return d_1
def calc_d_2(r, sigma, S, K, T, div = 0):
    """
    Calculate the value d2 in Black-Scholes model 

    : param r           : Risk-free interest rate 
    : param sigma       : Volatility 
    : param S           : Spot price of the underlying stock 
    : param K           : Strike price of the option
    : param T           : Time for maturity  
    : param div         : Dividends 
    : returns           : d2
    """
    d_2 = (np.log(S/K) + (r-div-sigma**2/2)*(T))/(sigma*np.sqrt(T))
    return d_2


def delta(r, sigma, S, K, T, call_or_put, div = 0):
    """
    Calculate the delta of an European option (Black-Scholes model) 

    : param r           : Risk-free interest rate 
    : param sigma       : Volatility 
    : param S           : Spot price of the underlying stock 
    : param K           : Strike price of the option
    : param T           : Time for maturity  
    : param call_or_put : Type of option: Call ('C') or Put ('P')
    : param div         : Dividends 
    : returns           : delta of the option 
    """
    d_1 = calc_d_1(r, sigma, S, K, T,  div = div)
    if (call_or_put == 'C'):
        return np.exp(-div*(T))*stats.norm.cdf(d_1)
    else:
        return -np.exp(-div*(T))*stats.norm.cdf(-d_1) 


def vega(r, sigma, S, K, T, call_or_put, div = 0):
    """
    Calculate the vega of an European option (Black-Scholes model) 

    : param r           : Risk-free interest rate 
    : param sigma       : Volatility 
    : param S           : Spot price of the underlying stock 
    : param K           : Strike price of the option
    : param T           : Time for maturity  
    : param call_or_put : Type of option: Call ('C') or Put ('P')
    : param div         : Dividends 
    : returns           : vega of the option 
    """
    d_1 = calc_d_1(r, sigma, S, K, T,  div = div)

    return S*np.exp(-div*(T))*stats.norm.pdf(d_1)*np.sqrt(T)


def theta(r, sigma, S, K, T, call_or_put, div = 0):
    """
    Calculate the theta of a european option (Black-Scholes model) 
    
    : param r           : Risk-free interest rate 
    : param sigma       : Volatility 
    : param S           : Spot price of the underlying stock 
    : param K           : Strike price of the option
    : param T           : Time for maturity  
    : param call_or_put : Type of option: Call ('C') or Put ('P')
    : param div         : Dividends 
    : returns           : theta of the option 
    """
    d_1 = calc_d_1(r, sigma, S, K, T,  div = div)
    d_2 = calc_d_2(r, sigma, S, K, T,  div = div) 
    # Obviamente esta función puede mejorar mucho,y lo hará 
    term_1 = -S*stats.norm.pdf(d_1)*sigma/(2*np.sqrt(T))
    if (call_or_put == 'C'):
        term_2 = -r*K*np.exp(-r*T)*stats.norm.cdf(d_2) 
 
    elif (call_or_put == 'P'):
        term_2 = r*K*np.exp(-r*T)*stats.norm.cdf(-d_2) 
    else: 
        raise ValueError("Please choose an appropiate value")
    return (term_1 + term_2 )

def gamma(r, sigma, S, K, T, call_or_put, div = 0):
    """
    Calculate the gamma of an European option (Black-Scholes model) 
    
    : param r           : Risk-free interest rate 
    : param sigma       : Volatility 
    : param S           : Spot price of the underlying stock 
    : param K           : Strike price of the option
    : param T           : Time for maturity  
    : param call_or_put : Type of option: Call ('C') or Put ('P')
    : param div         : Dividends 
    : returns           : gamma of the option 
    """
    d_1 = calc_d_1(r, sigma, S, K, T,  div = div) 
    return stats.norm.pdf(d_1)/(S*sigma*np.sqrt(T)) 

def rho(r, sigma, S, K, T, call_or_put, div = 0): 
    """
    Calculate the rho of an European option (Black-Scholes model) 

    : param r           : Risk-free interest rate 
    : param sigma       : Volatility 
    : param S           : Spot price of the underlying stock 
    : param K           : Strike price of the option
    : param T           : Time for maturity  
    : param call_or_put : Type of option: Call ('C') or Put ('P')
    : param div         : Dividends 
    : returns           :  rho of the option 
    """
    d_2 = calc_d_2(r, sigma, S, K, T,  div = div) 
    if (call_or_put == 'C'): 
        return K* (T)*np.exp(-r*T) * stats.norm.cdf(d_2) 
    elif call_or_put == 'P': 
        return -K* (T)*np.exp(-r*T) * stats.norm.cdf(-d_2) 
    else: 
        #error message
        pass 


def BSprice (r, sigma, S, K, T, call_or_put, div = 0):
    """
    Calculate the value of an European option (Black-Scholes model) 

    : param r           : Risk-free interest rate 
    : param sigma       : Volatility 
    : param S           : Spot price of the underlying stock 
    : param K           : Strike price of the option
    : param T           : Time for maturity  
    : param call_or_put : Type of option: Call ('C') or Put ('P')
    : param div         : Dividends 
    : returns           : Option value
    """
    d_1 = calc_d_1(r, sigma, S, K, T,  div = div) 
    d_2 = calc_d_2(r, sigma, S, K, T, div = div) 
    if (call_or_put == 'C'):
        V = S*np.exp(-div*(T))*stats.norm.cdf(d_1)-K*np.exp(-r*(T))*stats.norm.cdf(d_2) 
    elif (call_or_put == 'P'):
        V = -S*np.exp(-div*(T))*stats.norm.cdf(-d_1)+K*np.exp(-r*(T))*stats.norm.cdf(-d_2)
    
    return V 


