import numpy as np 
import yfinance 
import matplotlib.pyplot as plt 
import math 
import pandas as pd 


# This function calculates the log returns from a series of prices and thus compute the mean (as an approximation of mu) and the std (as an approximation of sigma)
def mu_sigma(prices):
  log_returns = np.zeros(len(log_prices)-1)
  for i in range(len(log_returns)):
    log_returns[i] = math.log(prices[i+1]/prices[i])
  mu = np.mean(log_returns)
  sigma = np.std(returns) 
  return (mu, sigma) 


#This function calculates GBM trajectories, steps is the number of steps and T the total time 
def gbm_trajectories(mu, sigma, T, steps, initial_value, num_trajectories = 10000):
  delta_t = T /steps
  S = np.zeros(num_trajectories, steps +1)   
  W = np.random.normal(0,1) 
  for i in range(num_trajectories):
    S[i,0] = initial_value 
  for i in range(num_trajectories);
    for j in range(time);
      S[i, j+1] = S[i,j] + mu*S[i,j] +sigma*S[i,j]*(math.sqrt(delta_t)*W[i,j])
  return S 

# Calculation of GBM trajectories using antithetic variates 

def gbm_ant_trajectories(mu, sigma, T, steps, initial_value, num_trajectories = 10000):
  delta_t = T /steps  
  S = np.zeros((num_trajectories, steps+1))
  ant_S = np.zeros((num_trajectories, steps+1))
  W = np.random.normal(0,1, (num_trajectories, steps+1))
  for i in range(num_trajectories): 
      S[i,0] = initial_value
      ant_S[i,0] = initial_value 
  for i in range(num_trajectories):
      for j in range(time):
          S[i][j+1] = S[i][j] + mu*S[i][j] + sigma*S[i][j] *(math.sqrt(delta_t) W[i][j])
          ant_S[i][j+1] = ant_S[i][j] + mu*ant_S[i][j] +sigma*ant_S[i][j] * (-math.sqrt(delta_t)*W[i][j])
    
  combined_S = np.concatenate((S, ant_S), axis = 0) 
  return combined_S 
