def EuPayOff(S, K, call_or_put):
    """
    Calculate the payoff of random paths of an European option

    : param S           : Numpy array of the paths 
    : param K           : Strike price
    : param call_or_put : Whether the option is a call ('C') or a put ('P') 
    : return            : numpy array containing the payoff of each path 
    """
    
    if call_or_put == 'C':
        return np.maximum(S[:,-1] - K, 0) 
    elif call_or_put =='P': 
        return np.maximum(K - S[:,-1], 0) 
    else: 
        raise ValueError("Please choose an appropiate value for call_or_put (Call ('C') or Put ('P')") 

def AsPayOff(S, K, call_or_put):
    """
    Calculate the payoff of random paths of an American option

    : param S           : Numpy array of the paths 
    : param K           : Strike price
    : param call_or_put : Whether the option is a price call ('PC'), a price put ('PP'), a strike call ('SC') or a strike put ('SP')  
    : return            : numpy array containing the payoff of each path 
    """
    
    
    A = np.zeros(S.shape[0]) 
    for i in range(len(A)): 
        A[i] = np.mean(S[i,:]) - S[i,0]/2 - S[i,-1]/2

    if call_or_put == 'PC': 
        return np.maximum(A - K, 0) 
    elif call_or_put == 'PP': 
        return np.maximum(K - A, 0) 
    elif call_or_put == 'SC': 
        return np.maximum(S[:,-1] - A, 0)
    elif call_or_put == 'SP':
        return np.maximum(A - S[:, -1], 0) 
    else: 
        raise ValueError("Please choose an appropiate value for call_or_Put (Price call ('PC'), Price put ('PP'), Strike call ('SK') or Strike put ('SP')") 
