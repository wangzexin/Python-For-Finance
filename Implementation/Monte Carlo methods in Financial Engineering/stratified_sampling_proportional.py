import numpy as np
import numpy.random as npr
import scipy.stats as scs

def stratified_sampling_european_call(strikePrice):
    # parameters
    sigma = 0.25;   T = 1.0;   I = 50000;   S0 = 100;   r = 0.05
    n = 50;   K = I / n;   totalEstimate = 0; pi = 1 / n; totalPayoffs = np.array([])
    # generate expectations at time T/2
    quantiles = [(2*x-1)/100 for x in range(1, n+1, 1)]
    standardNormals = scs.norm.ppf(quantiles, 0, 1)
    halfPrices = S0*np.exp((r-sigma**2/2)*T/2 + sigma * np.sqrt(T/2)*standardNormals)
    # generate I / n prices starting from the halfPrices
    for i in range(n):
        rand = np.random.standard_normal(I//n)
        finalPrices = halfPrices[i]*np.exp((r-sigma**2/2)*T/2+sigma*np.sqrt(T/2)*rand)
        payoffs = np.maximum(finalPrices - strikePrice, 0)
        totalPayoffs = np.append(totalPayoffs, payoffs)
        averagePayoffs = np.average(payoffs)
        totalEstimate += averagePayoffs * pi;
    totalEstimate *= np.exp(-r * T)
    totalPayoffsVariance = np.var(totalPayoffs)
    return (totalEstimate, totalPayoffsVariance)

def mcs_european_call(strikePrice):
    # parameters
    sigma = 0.25;   T = 1.0;   I = 50000;   S0 = 100;   r = 0.05
    totalEstimate = 0;    totalPayoffs = np.array([])
    rand = np.random.standard_normal(I)
    stockPrices = S0*np.exp((r-sigma**2/2)*T+sigma*np.sqrt(T)*rand)
    payoffs = np.maximum(stockPrices - strikePrice, 0)
    averagePayoffs = np.average(payoffs)
    totalEstimate = averagePayoffs * np.exp(-r * T)
    totalPayoffsVariance = np.var(payoffs)
    return (totalEstimate, totalPayoffsVariance)
