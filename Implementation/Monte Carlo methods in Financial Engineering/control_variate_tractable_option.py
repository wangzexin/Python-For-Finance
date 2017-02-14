import numpy as np
import numpy.random as npr
def control_variate_tractable_option_european_call(strikePrice, tractableOptionStrike):
    # parameters
    sigma = 0.25;   T = 1.0;   I = 50000;   S0 = 100;   r = 0.05
    #tractableOptionStrike = 2 * S0 - strikePrice
    # pilot simulation
    standardNormals = npr.standard_normal(I)
    stockPrices = S0*np.exp((r-sigma**2/2)*T+sigma*np.sqrt(T)*standardNormals)
    putOptionPayoffs = np.maximum(tractableOptionStrike - stockPrices, 0)
    optionPayoffs = np.maximum(stockPrices - strikePrice, 0)
    covarianceMatrix = np.cov(putOptionPayoffs, optionPayoffs)
    lambdaStar = covarianceMatrix[0][1] / covarianceMatrix[0][0]
    # main simulation
    standardNormals = npr.standard_normal(I)
    stockPrices = S0*np.exp((r-sigma**2/2)*T+sigma*np.sqrt(T)*standardNormals)
    putOptionPayoffs = np.maximum(tractableOptionStrike - stockPrices, 0)
    optionPayoffs = np.maximum(stockPrices - strikePrice, 0)
    averagePutOptionPayoffs = np.average(putOptionPayoffs) # use average as an estimate
    newPayoffs = optionPayoffs - lambdaStar * (putOptionPayoffs - averagePutOptionPayoffs)
    optionPayoffs *= np.exp(-r*T)
    newPayoffs *= np.exp(-r*T)
    oldEstimate = np.average(optionPayoffs)
    oldVariance = np.var(optionPayoffs)
    newEstimate = np.average(newPayoffs)
    estimateVariance = np.var(newPayoffs)
    return (oldEstimate, oldVariance, newEstimate, estimateVariance)
