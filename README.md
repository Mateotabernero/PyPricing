# PyPricing
PyPricing is an Option Pricing library written in Python. The library includes:

-  Pricing of European and American Option and computation of greeks: Binomial, MonteCarlo and Black-Scholes
-  Stock price models: GBM, Heston, Jump Diffusion (Jump Diffusion lo añadiré después si hay tiempo, antes dejaré todo preparado) 
-  Pricing of exotic options (Asian, )
-  Advanced techniques: FFT, COS transforms (También si hay tiempo)
-  Plotting of option price and greeks curves
- 



I intend to have four separate files for different types of functions. The files will be:
-  One file for common, simple functions like the payOff function or estimating the volatility for a given stock that may be used in the other three files
-  Another file for binomial option pricing and related (trinomial option pricing, etc)
-  A file for Montecarlo option pricing (based on different stock-price-evolution models like GBM, GBM + CIR, etc) (I'm also implementing several SDE numerical integration systems, like Euler-Maruyama, Milstein or Rudge-Kutta
-  A file for Black-Scholes option pricing and related, with methods for numerical integration of PDEs (and PIDEs in the future)

In each file I also want to implement methods for computing the greeks according to each method. I have already done it for two greeks for the binomial option pricing and it is pretty basic to do it for Montecarlo, it's just re-running the simulations with different initial conditions. So I will implement the computation of greeks with Monte-Carlo soon enough

