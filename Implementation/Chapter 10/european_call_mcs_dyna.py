import numpy as np
import numpy.random as npr

def gen_sn(M, I, anti_paths=True, mo_match=True):
    ''' Function to generate random numbers for simulation.
    Parameters
    M : int  number of time intervals for discretization
    I : int  number of paths to be simulated
    anti_paths: Boolean  use of antithetic variates
    mo_math : Boolean  use of moment matching'''
    if anti_paths is True: # "is True" is different from == True
        sn = npr.standard_normal((M + 1, I // 2)) # generate half, assuming I is even
        sn = np.concatenate((sn, -sn), axis=1) # add negative half
    else:
        sn = npr.standard_normal((M + 1, I))
    if mo_match is True:
        sn = (sn - sn.mean()) / sn.std()
    return sn

def gbm_mcs_dyna(K, M = 50, option='call', r = .05, sigma = .25):
    ''' Valuation of European options in Black-Scholes-Merton
    by Monte Carlo simulation (of index level paths)
    Parameters
    K : float    (positive) strike price of the option
    option : string    type of the option to be valued (‘call’, ‘put’)
    C0 : float    estimated present value of European call option
    '''
    T = 1.0;   I = 20000;   dt = T / M;   S0 = 100
    # simulation of index level paths
    S = np.zeros((M + 1, I))
    S[0] = S0
    sn = gen_sn(M, I)
    for t in range(1, M + 1):
        S[t] = S[t - 1] * np.exp((r - 0.5 * sigma ** 2) * dt
                                 + sigma * np.sqrt(dt) * sn[t])
    # case-based calculation of payoff
    if option == 'call':
        hT = np.maximum(S[-1] - K, 0)
    else:
        hT = np.maximum(K - S[-1], 0)
    # calculation of MCS estimator
    C0 = np.exp(-r * T) * 1 / I * np.sum(hT)
    return C0
