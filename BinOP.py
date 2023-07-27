import math
def beta (r, sigma, delta_t, gamma_par = 1): 
    return 1/2 *(gamma_par *math.exp(-r*delta_t) + math.exp((r+sigma**2)*delta_t))

def u(beta, gamma_par = 1): 
    return beta + math.sqrt(beta**2 - gamma_par) 
def d(beta, gamma_par= 1):
    return beta - math.sqrt(beta*+2 - gamma_par)

def p(r, delta_t, u, d):
    return (math.exp (r*delta_t)-d) / (u-d) 

# We need to put something if put_or_call is not P or C
def payOff (S,K, put_or_call, bound = 0): 
    if (put_or_call == 'C'): 
        max(S-K,bound) 
    elif (put_or_call == 'P'):
        max (K-S, bound) 

# To improve convergence choose gamma = e^((2/M)*log(K/S_0))

def binOP (r, sigma, S, T, K, put_or_call, optionType, M): 
    
    # Compute delta_t 
    delta_t = T / M 

    # Creation of the tree of stock prices and the tree of option value (We don't really need to create the price tree, we just need the last one. the second s array is that case) (For american ption is necessary)
    # No ahorraríamos mucho si metemos lo de S dentro de los if, porque ya estamos haciendo O(M^2) work anyways 
    S = [[0 for _ in range (i+1)] for i in range (M+1)] 
    V = [[0 for _ in range (i+1)] for i in range (M+1)]
    V_cont = [[0 for _ in range(i+1)] for i in range(M+1)]
    
    
    # Boundary values

    S[0,0] = S 
    for j in range (M+1): 
        S[j, M] = S[0,0] * (u**j) * (d** (M-j)) 
        
    
    for j in range (M+1):
        V[j,M]   = payOff(S[j,M], K, put_or_call)
        
    
    if optionType == 'E':
        for i in reversed(range (M)):
            for j in range(i):
                V[j,i] = math.exp(-r*delta_t)*(p*V[j+1,i+1] + (1-p)*V[j, i+1])

    
    elif optionType == 'A':
        for i in reversed(range(M)):
            for j in range(i):
                S[j,i] = S[0,0] * (u**j) * (d** (i-j))
                V_cont[j,i] = math.exp(-r*delta_t) *(p*V[j+1, i+1] + (1-p)*V[j,i+1])
                V[j,i]      = payOff (S[j,i],K,put_or_call, bound = V_cont[j,i])        

    else:
        raise ValueError ("optionType has to be European ('E') or American ('A')")

    return V[0,0]
