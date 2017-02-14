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

def gbm_mcs_amer(K, S0=100, T=1, M=50, I= 20000, option='call', r=.05, sigma=.25):
    ''' Valuation of American option in Black-Scholes-Merton by MCS LSM
    K : float    (positive) strike price of the option
    option : string    type of the option to be valued (‘call’, ‘put’)
    C0 : float    estimated present value of European call option    '''
    dt = T / M;    df = np.exp(-r * dt)
    # simulation of index levels
    S = np.zeros((M + 1, I));    S[0] = S0;    sn = gen_sn(M, I)
    for t in range(1, M + 1):
        S[t] = S[t - 1] * np.exp((r - 0.5 * sigma ** 2) * dt
        + sigma * np.sqrt(dt) * sn[t])
    if option == 'call': # case-based calculation of payoff
        h = np.maximum(S - K, 0)
    else:
        h = np.maximum(K - S, 0)
    # LSM algorithm
    V = np.copy(h)
    for t in range(M - 1, 0, -1):
        reg = np.polyfit(S[t], V[t + 1] * df, 7)
        C = np.polyval(reg, S[t])
        V[t] = np.where(C > h[t], V[t + 1] * df, h[t])
    C0 = df * 1 / I * np.sum(V[1]) # MCS estimator
    return C0
