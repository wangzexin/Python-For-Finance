import numpy as np
import numpy.random as npr
import scipy.stats as scs

def VaR_stock_price(S0=100, r=.05, sigma=.25, T=30/365, I=10000):
    ST = S0*np.exp((r-0.5*sigma**2)*T+sigma*np.sqrt(T)*npr.standard_normal(I))
    R_gbm = np.sort(ST - S0) / S0
    percs = [0.01, 0.1, 1., 2.5, 5.0, 10.0]
    var = scs.scoreatpercentile(R_gbm, percs)
    print("%16s %16s" % ('Confidence Level', 'Value-at-Risk'))
    print(33 * "-")
    for pair in zip(percs, var):
        print("%16.2f %16.3f" % (100 - pair[0], -pair[1]))
