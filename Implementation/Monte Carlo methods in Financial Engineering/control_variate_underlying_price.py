import numpy as np
import numpy.random as npr
def control_variate_underlying_assets_european_call(strikePrice):
    # parameters
    sigma = 0.25;   T = 1.0;   I = 500000;   S0 = 100;   r = 0.05
    # pilot simulation
    standardNormals = npr.standard_normal(I)
    stockPrices = S0*np.exp((r-sigma**2/2)*T+sigma*np.sqrt(T)*standardNormals)
    optionPayoffs = np.maximum(stockPrices - strikePrice, 0)
    covarianceMatrix = np.cov(stockPrices, optionPayoffs)
    lambdaStar = covarianceMatrix[0][1] / covarianceMatrix[0][0]
    # main simulation
    standardNormals = npr.standard_normal(I)
    stockPrices = S0*np.exp((r-sigma**2/2)*T+sigma*np.sqrt(T)*standardNormals)
    optionPayoffs = np.maximum(stockPrices - strikePrice, 0)
    # Replace np.exp(r*T-sigma**2/2)*S0 with np.average(stockPrices)
    newPayoffs = optionPayoffs - lambdaStar * (stockPrices - np.average(stockPrices))
    optionPayoffs *= np.exp(-r*T)
    newPayoffs *= np.exp(-r*T)
    oldEstimate = np.average(optionPayoffs)
    oldVariance = np.var(optionPayoffs)
    newEstimate = np.average(newPayoffs)
    estimateVariance = np.var(newPayoffs)
    return (oldEstimate, oldVariance, newEstimate, estimateVariance)
