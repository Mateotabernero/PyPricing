import math

### We first include some functions to compute some useful magnitudes on Binomial Option pricing 

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
    return (math.exp (r*delta_t)-d) / (u-d) 

# We need to put something if put_or_call is not P or C
def payOff (S,K, put_or_call, bound = 0): 
    if (put_or_call == 'C'): 
        return max(S-K,bound) 
    elif (put_or_call == 'P'):
        return max (K-S, bound) 

# To improve convergence choose gamma = e^((2/M)*log(K/S_0))

def binOP (r, sigma, initial_S, T, K, put_or_call, optionType, M, gamma_par = 1): 
    # Compute delta_t 
    delta_t = T / M 
    
    beta = calc_beta(r, sigma, delta_t, gamma_par = gamma_par )
    u = calc_u(beta, gamma_par = gamma_par ) 
    d = calc_d (beta, gamma_par = gamma_par) 
    p = calc_p (r, delta_t, u, d)

    # Creation of the tree of stock prices and the tree of option value (We don't really need to create the price tree, we just need the last one. the second s array is that case) (For american ption is necessary)
    # No ahorraríamos mucho si metemos lo de S dentro de los if, porque ya estamos haciendo O(M^2) work anyways 
    S= [[0 for _ in range (i+1)] for i in range (M+1)] 
    V = [[0 for _ in range (i+1)] for i in range (M+1)]
    V_cont = [[0 for _ in range(i+1)] for i in range(M+1)]
    
    
    # Boundary values

    S[0][0] = initial_S 
    for j in range (M+1): 
        S[M][j] = S[0][0] * (u**j) * (d** (M-j)) 
        
    
    for j in range (M+1):
        
        V[M][j]   = payOff(S[M][j], K, put_or_call)

    if optionType == 'E':
        for i in reversed(range (M)):
            for j in range(i):
                V[i][j] = math.exp(-r*delta_t)*(p*V[i+1][j+1] + (1-p)*V[i+1][j])

    
    elif optionType == 'A':
        for i in reversed(range(M)):
            for j in range(i+1):
                S[i][j] = S[0][0] * (u**j) * (d** (i-j))
                
                V_cont[i][j] = math.exp(-r*delta_t) *(p*(V[i+1][j+1]) + (1-p)*V[i+1][j])
                V[i][j]      = max(payOff (S[i][j],K,put_or_call), V_cont[i][j])       

    else:
        raise ValueError ("optionType has to be European ('E') or American ('A')")
    # greek estimations (pretty rough) 
    delta = (V[1][1]- V[1][0]) / (S[1][1] -S[1][0])
    # Para gamma quiero mirarme primero mejor como se hace el tema de finite differences con segundas derivadas. Tenemos calculadas dos por lo menos  
    theta = (V[2][1] - V[0][0]) / (2*delta_t)


    return V[0][0]
    
