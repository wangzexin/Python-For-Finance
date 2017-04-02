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
        print(europeanPut(100, i, 1, 0.05, 0.25))

def barrierCallOption(S, K, B, h, r, sigma):
    if B < K:
        result1 = europeanCall(S, K, h, r, sigma)
        result2 = (B / S) ** (2*r/(sigma**2)-1) * europeanCall(B**2/S, K, h, r, sigma)
        return result1 - result2
    else:
        d5 = (np.log(S/B) + (r + sigma**2/2) * h) / (sigma * h ** 0.5)
        d6 = d5 - sigma * h ** 0.5
        d7 = (np.log(B/S) + (r + sigma**2/2) * h) / (sigma * h ** 0.5)
        d8 = d7 - sigma * h ** 0.5
        N5 = scs.norm.cdf(d5)
        N6 = scs.norm.cdf(d6)
        N7 = scs.norm.cdf(d7)
        N8 = scs.norm.cdf(d8)
        result1 = S * N5 - K * np.exp(-r * h) * N6
        result3 = (B/S)**(2*r/(sigma**2)+1) * S * N7
        result2 = (B/S)**(2*r/(sigma**2)-1) * K * np.exp(-r * h) * N8
        return result1 + result2 - result3

def testBarrierDownOutCall():
    for i in range(70, 170, 10):
        print(str(i)+"&",end="")
        for j in range(75, 125, 10):
            print(str(round(barrierCallOption(100, i, j, 1, 0.05, 0.25),10))+'&', end="")
        print()
