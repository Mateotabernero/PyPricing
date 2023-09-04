import math

### We first include some functions to compute some useful magnitudes on Binomial Option pricing (all to be explained in the Readme file) 
def payOff (S,K, put_or_call):
    """
    Calculate the payoff of an American or European option at some moment

    : param S            : Current price of the underlying stock
    : param K            : Exercise price 
    : param put_or_call  : Is the option a put ('P') or a call ('C')?
    : return             : payoff of the option 
    """
    if (put_or_call == 'C'): 
        return np.maximum(S-K,0) 
    elif (put_or_call == 'P'):
        return np.maximum(K-S, 0) 
    else: 
        raise ValueError ("Please choose a valid value for put_or_call: Put ('P') or Call ('C')") 
        
def calc_beta (r, sigma, delta_t, gamma_par = 1): 
    """
    Calculate beta in Binomial Option Pricing 
    : param r            : Risk-free interest rate
    : param sigma        : Volatility of the stock price
    : param delta_t      : Time increments in the Binomial Option Pricing tree 
    : oaram gamma_par    : The gamma parameter in BOP (default value: 1) 
    : return             : beta 
    """
    return 1/2 *(gamma_par *math.exp(-r*delta_t) + math.exp((r+sigma**2)*delta_t))

def calc_u(beta, gamma_par = 1): 
    """
    Calculate u in Binomial Option Pricing
    : param beta         : beta 
    : param gamma_par    : The gamma parameter in BOP (default value: 1) 
    : return             : u, the factor by which S moves up in Binomial Option Pricing
    """
    return (beta + math.sqrt(beta**2 - gamma_par)) 
    
def calc_d(beta, gamma_par= 1):
    """
    Calculate d in Binomial Option Pricing
    : param beta         : beta 
    : param gamma_par    : The gamma parameter in BOP (default value: 1) 
    : return             : d, the factor by which S moves down in BOP 
    """
    return (beta - math.sqrt(beta**2 - gamma_par))

def calc_p(r, delta_t, u, d):
    """
    Calculate p in Binomial Option Pricing 
    : param r            : Risk-free interest rate 
    : param delta_t      : Time increments 
    : param u            : u, the factor by which S moves up in BOP 
    : param d            : d, the factor by which S moves down in BOP
    : return             : p, the probability of S moving up 
    """
    return (math.exp (r*delta_t)-d) / (u-d) 


# To improve convergence choose gamma = e^((2/M)*log(K/S_0)) is a good choice

def binOP (r, sigma, S, T, K, put_or_call, optionType, M, gamma_par = 1): 

    """
    Calculate the value of an American or European option using Binomial Method 
    : param r            : Risk-free interest rate 
    : param sigma        : Volatility 
    : param S            : Price of the underlying stock 
    : param T            : Expiration time 
    : K                  : Strike price
    : param put_or_call  : Put ('P') or Call ('C') 
    : param optionType   : Is it an European ('E') or American ('A') option? 
    : param M            : Number of steps in the binomial tree 
    : param gamma_par    : Gamma parameter in binomial option pricing (default value: 1) 
    : return            : Value of the option 
    """
    # Compute delta_t 
    delta_t = T / M 
    
    beta = calc_beta(r, sigma, delta_t, gamma_par = gamma_par )
    u = calc_u(beta, gamma_par = gamma_par ) 
    d = calc_d (beta, gamma_par = gamma_par) 
    p = calc_p (r, delta_t, u, d)

    # Creation of the tree of stock prices and the tree of option value (We don't really need to create the price tree, we just need the last one. the second s array is that case) (For american ption is necessary)

    S= [[0 for _ in range (i+1)] for i in range (M+1)] 
    V = [[0 for _ in range (i+1)] for i in range (M+1)]
    V_cont = [[0 for _ in range(i+1)] for i in range(M+1)]
    
    
    # Boundary values

    S[0][0] = S_0
    for j in range (M+1): 
        S[M][j] = S[0][0] * (u**j) * (d** (M-j)) 
        
    
    for j in range (M+1):
        
        V[M][j]   = payOff(S[M][j], K, put_or_call)

    if optionType == 'E':
        for i in reversed(range (M)):
            for j in range(i+1):
                S[i][j] = S[0][0] * (u**j) * (d** (i-j))
                
                V[i][j] = math.exp(-r*delta_t)*(p*V[i+1][j+1] + (1-p)*V[i+1][j])

    
    elif optionType == 'A':
        for i in reversed(range(M)):
            for j in range(i+1):
                S[i][j] = S[0][0] * (u**j) * (d** (i-j))
                
                V_cont[i][j] = math.exp(-r*delta_t) *(p*(V[i+1][j+1]) + (1-p)*V[i+1][j])
                V[i][j]      = max(payOff (S[i][j],K,put_or_call), V_cont[i][j])       

    else:
        raise ValueError ("optionType has to be European ('E') or American ('A')")
    
    # Computing greeks:  
    delta = (V[1][1]- V[1][0]) / (S[1][1] -S[1][0])
    theta = (V[2][1] - V[0][0]) / (2*delta_t)
    # (Include gamma and other greeks) 
    return V[0][0]

def generate_tree(r, sigma, S_0, T, K, put_or_call, optionType, M, gamma_par = 1): 
    """
    Calculate the Binomial Tree for American or European option 
    : param r            : Risk-free interest rate 
    : param sigma        : Volatility 
    : param S            : Price of the underlying stock 
    : param T            : Expiration time 
    : K                  : Strike price
    : param put_or_call  : Put ('P') or Call ('C') 
    : param optionType   : Is it an European ('E') or American ('A') option? 
    : param M            : Number of steps in the binomial tree 
    : param gamma_par    : Gamma parameter in binomial option pricing (default value: 1) 
    : return             : Tree
    """
    # Compute delta_t 
    delta_t = T / M 
    
    beta = calc_beta(r, sigma, delta_t, gamma_par = gamma_par )
    u = calc_u(beta, gamma_par = gamma_par ) 
    d = calc_d (beta, gamma_par = gamma_par) 
    p = calc_p (r, delta_t, u, d)

    # Creation of the tree of stock prices and the tree of option value (We don't really need to create the price tree, we just need the last one. the second s array is that case) (For american ption is necessary)

    S= [[0 for _ in range (i+1)] for i in range (M+1)] 
    V = [[0 for _ in range (i+1)] for i in range (M+1)]
    V_cont = [[0 for _ in range(i+1)] for i in range(M+1)]
    
    
    # Boundary values

    S[0][0] = S_0
    for j in range (M+1): 
        S[M][j] = S[0][0] * (u**j) * (d** (M-j)) 
        
    
    for j in range (M+1):
        
        V[M][j]   = payOff(S[M][j], K, put_or_call)

    if optionType == 'E':
        for i in reversed(range (M)):
            for j in range(i+1):
                S[i][j] = S[0][0] * (u**j) * (d** (i-j))
                V[i][j] = math.exp(-r*delta_t)*(p*V[i+1][j+1] + (1-p)*V[i+1][j])

    
    elif optionType == 'A':
        for i in reversed(range(M)):
            for j in range(i+1):
                S[i][j] = S[0][0] * (u**j) * (d** (i-j))
                
                V_cont[i][j] = math.exp(-r*delta_t) *(p*(V[i+1][j+1]) + (1-p)*V[i+1][j])
                V[i][j]      = max(payOff (S[i][j],K,put_or_call), V_cont[i][j])       

    else:
        raise ValueError ("optionType has to be European ('E') or American ('A')")
    return V 

def valueBinOp(r, sigma, S, T, K, put_or_call, optionType, M, gamma_par = 1): 
    V, S = generate_tree(r, sigma, S, T, K, put_or_call, optionType, M, gamma_par = gamma_par)
    return V[0][0]
