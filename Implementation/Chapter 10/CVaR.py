import numpy as np
import numpy.random as npr

def CVaR():
    S0 = 100.
    r = 0.05
    sigma = 0.2
    T = 1.
    I = 100000
    ST = S0 * np.exp((r - 0.5 * sigma ** 2) * T
                     + sigma * np.sqrt(T) * npr.standard_normal(I))
    L = 0.5
    p = 0.01
    D = npr.poisson(p * T, I)
    D = np.where(D > 1, 1, D)
    CVaR = np.exp(-r * T) * 1 / I * np.sum(L * D * ST)
    S0_CVA = np.exp(-r * T) * 1 / I * np.sum((1 - L * D) * ST)
    S0_adj = S0 - CVaR
    return (CVaR, S0_CVA, S0_adj)
