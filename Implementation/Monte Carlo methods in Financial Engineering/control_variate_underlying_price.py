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
    newPayoffs = optionPayoffs - lambdaStar * (stockPrices - S0 * np.exp(r*T))
    optionPayoffs *= np.exp(-r*T)
    newPayoffs *= np.exp(-r*T)
    oldEstimate = np.average(optionPayoffs)
    oldVariance = np.var(optionPayoffs)
    newEstimate = np.average(newPayoffs)
    estimateVariance = np.var(newPayoffs)
    return (oldEstimate, oldVariance, newEstimate, estimateVariance)

def testCall():
    for i in range(105, 205, 5):
        print(control_variate_underlying_assets_european_call(i))

def control_variate_underlying_assets_european_put(strikePrice):
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
    optionPayoffs = np.maximum(strikePrice - stockPrices, 0)
    # Replace np.exp(r*T-sigma**2/2)*S0 with np.average(stockPrices)
    newPayoffs = optionPayoffs - lambdaStar * (stockPrices - S0 * np.exp(r*T))
    optionPayoffs *= np.exp(-r*T)
    newPayoffs *= np.exp(-r*T)
    oldEstimate = np.average(optionPayoffs)
    oldVariance = np.var(optionPayoffs)
    newEstimate = np.average(newPayoffs)
    estimateVariance = np.var(newPayoffs)
    return (oldEstimate, oldVariance, newEstimate, estimateVariance)

def testPut():
    for i in range(105, 205, 5):
        print(control_variate_underlying_assets_european_put(i))

def convergence_control_variate_underlying_assets_european_call(strikePrice):
    # parameters
    sigma = 0.25;   T = 1.0;   I = 10000000;   S0 = 100;   r = 0.05
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
    newPayoffs = optionPayoffs - lambdaStar * (stockPrices - S0 * np.exp(r*T))
    optionPayoffs *= np.exp(-r*T)
    newPayoffs *= np.exp(-r*T)
    oldEstimate = list(optionPayoffs)
    newEstimate = list(newPayoffs)
    totalOld = 0
    totalNew = 0
    old = []
    new = []
    for i in range(I):
        totalOld += oldEstimate[i]
        totalNew += newEstimate[i]
        if (i+1) % 100000 == 0:
            old.append(totalOld / (i+1))
            new.append(totalNew / (i+1))
    points = [x * 100000 for x in range(101)]
    for i in range(100):
        print(points[i+1], "&", old[i], "&", new[i], "\\\\")
    #return (points, old, new)

def convergence_control_variate_underlying_assets_european_put(strikePrice):
    # parameters
    sigma = 0.25;   T = 1.0;   I = 10000000;   S0 = 100;   r = 0.05
    # pilot simulation
    standardNormals = npr.standard_normal(I)
    stockPrices = S0*np.exp((r-sigma**2/2)*T+sigma*np.sqrt(T)*standardNormals)
    optionPayoffs = np.maximum(strikePrice - stockPrices, 0)
    covarianceMatrix = np.cov(stockPrices, optionPayoffs)
    lambdaStar = covarianceMatrix[0][1] / covarianceMatrix[0][0]
    # main simulation
    standardNormals = npr.standard_normal(I)
    stockPrices = S0*np.exp((r-sigma**2/2)*T+sigma*np.sqrt(T)*standardNormals)
    optionPayoffs = np.maximum(strikePrice - stockPrices, 0)
    # Replace np.exp(r*T-sigma**2/2)*S0 with np.average(stockPrices)
    newPayoffs = optionPayoffs - lambdaStar * (stockPrices - S0 * np.exp(r*T))
    optionPayoffs *= np.exp(-r*T)
    newPayoffs *= np.exp(-r*T)
    oldEstimate = list(optionPayoffs)
    newEstimate = list(newPayoffs)
    totalOld = 0
    totalNew = 0
    old = []
    new = []
    for i in range(I):
        totalOld += oldEstimate[i]
        totalNew += newEstimate[i]
        if (i+1) % 100000 == 0:
            old.append(totalOld / (i+1))
            new.append(totalNew / (i+1))
    points = [x * 100000 for x in range(101)]
    for i in range(100):
        print(points[i+1], "&", old[i], "&", new[i], "\\\\")
    #return (points, old, new)
