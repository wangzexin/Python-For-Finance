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

def gbm_mcs_stat(K, S0 = 100, r = 0.05, sigma = 0.25, T = 1.0, I = 50000):
    ''' Valuation of European call option in Black-Scholes-Merton
    by Monte Carlo simulation (of index level at maturity)
    Parameters
    ==========
    K : float    (positive) strike price of the option
    C0 : float    estimated present value of European call option
    '''
    sn = gen_sn(1, I)
    # simulate index level at maturity
    ST = S0 * np.exp((r - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * sn[1])
    # calculate payoff at maturity
    hT = np.maximum(ST - K, 0)
    # calculate MCS estimator
    C0 = np.exp(-r * T) * 1 / I * np.sum(hT)
    return C0
