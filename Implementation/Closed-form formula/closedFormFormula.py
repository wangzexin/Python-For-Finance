import numpy as np
import scipy.stats as scs

def europeanCall(St, K, h, r, sigma):
    d2 = (np.log(St / K) + (r - sigma ** 2 / 2) * h) / (sigma * h ** 0.5)
    d1 = d2 + sigma * h ** 0.5
    N1 = scs.norm.cdf(d1)
    N2 = scs.norm.cdf(d2)
    return St * N1 - K * np.exp(-r * h) * N2
