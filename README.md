# PyPricing
PyPricing is an Option Pricing library written in Python. The library includes:

-  Pricing of European and American Option and computation of greeks: Binomial, MonteCarlo and Black-Scholes
-  Stock price models: GBM, Heston, Jump Diffusion (Jump Diffusion lo añadiré después si hay tiempo, antes dejaré todo preparado) 
-  Pricing of exotic options (Asian, )
-  Advanced techniques: FFT, COS transforms (También si hay tiempo)
-  Plotting of option price and greeks curves
- 


In each file I also want to implement methods for computing the greeks according to each method. I have already done it for two greeks for the binomial option pricing and it is pretty basic to do it for Montecarlo, it's just re-running the simulations with different initial conditions. So I will implement the computation of greeks with Monte-Carlo soon enough

## helpFunction 
The helpFunction.py contains functions that are useful for the other files. Those function being: 

- payOff         : Calculates the (vanilla) payoff of an American or European option at a given time
- asianPayOff    : Computes the payoff of an Asian option
- mu_sigma       : Computes mean and standard deviation of log returns of a given stock 
