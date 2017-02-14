import numpy as np
import numpy.random as npr

def srd_exact():
    x0 = 0.05; kappa = 3.0; theta = 0.02; sigma = 0.1 # model parameters
    I = 10000; M = 50; T = 1; dt = T / M # time parameters
    x2 = np.zeros((M + 1, I));    x2[0] = x0
    c = (sigma ** 2 * (1 - np.exp(-kappa * dt))) / (4 * kappa)
    df = 4 * theta * kappa / sigma ** 2 # degree of freedom
    for t in range(1, M + 1):
        nc = np.exp(-kappa * dt) / c * x2[t - 1] #noncentrality parameter
        x2[t] = c * npr.noncentral_chisquare(df, nc, size=I)
    return x2
x2 = srd_exact()
