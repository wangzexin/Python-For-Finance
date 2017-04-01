import numpy as np
import scipy.stats as scs

def europeanCall(St, K, h, r, sigma):
    d2 = (np.log(St / K) + (r - sigma ** 2 / 2) * h) / (sigma * h ** 0.5)
    d1 = d2 + sigma * h ** 0.5
    N1 = scs.norm.cdf(d1)
    N2 = scs.norm.cdf(d2)
    return St * N1 - K * np.exp(-r * h) * N2

def testCall():
    for i in range(105, 205, 5):
        print(europeanCall(100, i, 1, 0.05, 0.25))

def europeanPut(St, K, h, r, sigma):
    d2 = (np.log(St / K) + (r - sigma ** 2 / 2) * h) / (sigma * h ** 0.5)
    d1 = d2 + sigma * h ** 0.5
    N1 = scs.norm.cdf(-d1)
    N2 = scs.norm.cdf(-d2)
    return K * np.exp(-r * h) * N2 - St * N1

def testPut():
    for i in range(105, 205, 5):
        print(europeanPut(100, i, 1, 0.05, 0.25), ",")

