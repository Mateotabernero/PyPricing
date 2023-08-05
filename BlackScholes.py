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
