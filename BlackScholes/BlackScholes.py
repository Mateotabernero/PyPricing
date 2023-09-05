import numpy as np 
import math 
import scipy.stats as stats

def calc_d_1(K, S, r, T, sigma, div = 0):
    """
    Calculate the value d1 in Black-Scholes model

    : param K           : Strike price of the option 
    : param S           : Spot price of the underlying stock 
    : param r           : Risk-free interest rate 
    : param T           : Time for maturity  
    : param sigma       : Volatility 
    : param call_or_put : Type of option: Call ('C') or Put ('P')
    : param div         : Dividends 
    : returns           : d1
    """
    d_1 = (math.log(S/K) + (r-div+sigma**2/2)*(T))/(sigma*math.sqrt(T))
    return d_1
def calc_d_2(K, S, r, T, sigma,  div = 0):
    """
    Calculate the value d2 in Black-Scholes model 

    : param K           : Strike price of the option 
    : param S           : Spot price of the underlying stock 
    : param r           : Risk-free interest rate 
    : param T           : Time for maturity  
    : param sigma       : Volatility 
    : param call_or_put : Type of option: Call ('C') or Put ('P')
    : param div         : Dividends 
    : returns           : d2
    """
    d_2 = (math.log(S/K) + (r-div-sigma**2/2)*(T))/(sigma*math.sqrt(T))
    return d_2


def delta(K, S, r, T, sigma, call_or_put, div = 0):
    """
    Calculate the delta of an European option (Black-Scholes model) 

    : param K           : Strike price of the option 
    : param S           : Spot price of the underlying stock 
    : param r           : Risk-free interest rate 
    : param T           : Time for maturity  
    : param sigma       : Volatility 
    : param call_or_put : Type of option: Call ('C') or Put ('P')
    : param div         : Dividends 
    : returns           : delta of the option 
    """
    d_1 = calc_d_1(K, S, r, T, sigma, div = div)
    if (call_or_put == 'C'):
        return math.exp(-div*(T))*stats.norm.cdf(d_1)
    else:
        return -math.exp(-div*(T))*stats.norm.cdf(-d_1) 


def vega(K, S, r, T, sigma, call_or_put, div = 0):
    """
    Calculate the vega of an European option (Black-Scholes model) 

    : param K           : Strike price of the option 
    : param S           : Spot price of the underlying stock 
    : param r           : Risk-free interest rate 
    : param T           : Time for maturity  
    : param sigma       : Volatility 
    : param call_or_put : Type of option: Call ('C') or Put ('P')
    : param div         : Dividends 
    : returns           : vega of the option 
    """
    d_1 = calc_d_1(K, S, r, T, sigma,  div = div)

    return S*math.exp(-div*(T))*stats.norm.pdf(d_1)*math.sqrt(T)


def theta(K, S, r, T, sigma, call_or_put, div = 0):
    """
    Calculate the theta of a european option (Black-Scholes model) 
    
    : param K           : Strike price of the option 
    : param S           : Spot price of the underlying stock 
    : param r           : Risk-free interest rate 
    : param T           : Time for maturity  
    : param sigma       : Volatility 
    : param call_or_put : Type of option: Call ('C') or Put ('P')
    : param div         : Dividends 
    : returns           : theta of the option 
    """
    d_1 = calc_d_1(K, S, r, T, sigma, div = div)
    d_2 = calc_d_2(K, S, r, T, sigma, div = div) 
    # Obviamente esta función puede mejorar mucho,y lo hará 
    term_1 = -S*stats.norm.pdf(d_1)*sigma/(2*math.sqrt(T))
    if (call_or_put == 'C'):
        term_2 = -r*K*math.exp(-r*T)*stats.norm.cdf(d_2) 
 
    elif (call_or_put == 'P'):
        term_2 = r*K*math.exp(-r*T)*stats.norm.cdf(-d_2) 
    else: 
        raise ValueError("Please choose an appropiate value")
    return (term_1 + term_2 )

def gamma(K, S, r, T, sigma, call_or_put, div = 0):
    """
    Calculate the gamma of an European option (Black-Scholes model) 
    
    : param K           : Strike price of the option 
    : param S           : Spot price of the underlying stock 
    : param r           : Risk-free interest rate 
    : param T           : Time for maturity  
    : param sigma       : Volatility 
    : param call_or_put : Type of option: Call ('C') or Put ('P')
    : param div         : Dividends 
    : returns           : gamma of the option 
    """
    d_1 = calc_d_1(K, S, r, T, sigma, div = div) 
    return stats.norm.pdf(d_1)/(S*sigma*math.sqrt(T)) 

def rho(K, S, r, T, sigma, call_or_put, div = 0): 
    """
    Calculate the rho of an European option (Black-Scholes model) 
    
    : param K           : Strike price of the option 
    : param S           : Spot price of the underlying stock 
    : param r           : Risk-free interest rate 
    : param T           : Time for maturity  
    : param sigma       : Volatility 
    : param call_or_put : Type of option: Call ('C') or Put ('P')
    : param div         : Dividends 
    : returns           :  rho of the option 
    """
    d_2 = calc_d_2(K, S, r, T, sigma, div = div) 
    if (call_or_put == 'C'): 
        return K* (T)*math.exp(-r*T) * stats.norm.cdf(d_2) 
    elif call_or_put == 'P': 
        return -K* (T)*math.exp(-r*T) * stats.norm.cdf(-d_2) 
    else: 
        #error message
        pass 


def BSprice (K,S,r, T, sigma, call_or_put, div = 0):
    """
    Calculate the value of an European option (Black-Scholes model) 

    : param K           : Strike price of the option 
    : param S           : Spot price of the underlying stock 
    : param r           : Risk-free interest rate 
    : param T           : Time for maturity  
    : param sigma       : Volatility 
    : param call_or_put : Type of option: Call ('C') or Put ('P')
    : param div         : Dividends 
    : returns           : Option value
    """
    d_1 = calc_d_1(K, S, r, T, sigma,  div = div) 
    d_2 = calc_d_2(K, S, r, T, sigma,  div = div) 
    if (call_or_put == 'C'):
        V = S*math.exp(-div*(T))*stats.norm.cdf(d_1)-K*math.exp(-r*(T))*stats.norm.cdf(d_2) 
    elif (call_or_put == 'P'):
        V = -S*math.exp(-div*(T))*stats.norm.cdf(-d_1)+K*math.exp(-r*(T))*stats.norm.cdf(-d_2)
    
    return V 
