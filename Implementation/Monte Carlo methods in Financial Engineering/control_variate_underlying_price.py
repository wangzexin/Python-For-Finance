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
    newPayoffs = optionPayoffs - lambdaStar * (stockPrices - np.average(stockPrices))
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

def control_variate_underlying_assets_down_out_call(S, strikePrice, barrier, T, r, sigma):
    # parameters
    I = 5000;   n = 500;    dt = T / n;     S0 = S
    optionPayoffs = []
    stockPrices = []
    # pilot simulation
    for i in range(0, I):
        standardNormals = list(npr.standard_normal(n))
        stockPrice = S0
        flag = True
        for j in range(0, n):
            stockPrice = stockPrice*np.exp((r-sigma**2/2)*dt+sigma*np.sqrt(dt)*standardNormals[j])
            if stockPrice < barrier:
                flag = False
        if flag:
            optionPayoffs.append(max(stockPrice - strikePrice, 0))
        else:
            optionPayoffs.append(0)
        stockPrices.append(stockPrice)
    optionPayoffs = np.array(optionPayoffs)
    stockPrices = np.array(stockPrices)
    covarianceMatrix = np.cov(stockPrices, optionPayoffs)
    lambdaStar = covarianceMatrix[0][1] / covarianceMatrix[0][0]
    
    # main simulation
    optionPayoffs = []
    stockPrices = []
    for i in range(0, I):
        standardNormals = list(npr.standard_normal(n))
        stockPrice = S0
        flag = True
        for j in range(0, n):
            stockPrice = stockPrice*np.exp((r-sigma**2/2)*dt+sigma*np.sqrt(dt)*standardNormals[j])
            if stockPrice < barrier:
                flag = False
        if flag:
            optionPayoffs.append(max(stockPrice - strikePrice, 0))
        else:
            optionPayoffs.append(0)
        stockPrices.append(stockPrice)
    optionPayoffs = np.array(optionPayoffs)
    stockPrices = np.array(stockPrices)
    newPayoffs = optionPayoffs - lambdaStar * (stockPrices - np.average(stockPrices))
    optionPayoffs *= np.exp(-r*T)
    newPayoffs *= np.exp(-r*T)
    oldEstimate = np.average(optionPayoffs)
    oldVariance = np.var(optionPayoffs)
    newEstimate = np.average(newPayoffs)
    estimateVariance = np.var(newPayoffs)
    return (oldEstimate, oldVariance, newEstimate, estimateVariance)
