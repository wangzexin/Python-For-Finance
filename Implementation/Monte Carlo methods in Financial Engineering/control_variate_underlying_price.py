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

import math
import random

def barrier_down_out_call(S, strikePrice, barrier, T, r, sigma):
    # parameters
    I = 50000;   n = 200;    dt = T / n;     S0 = S
    barrier = barrier * math.exp(0.5826 * sigma * dt ** 0.5)
    totalPayoff = 0
    for i in range(0, I):
        stockPrice = S0 + 1 - 1
        flag = True
        for j in range(0, n):
            z = random.normalvariate(0, 1)
            stockPrice = stockPrice*math.exp((r-sigma**2/2)*dt+sigma*dt**0.5*z)
            if stockPrice < barrier:
                flag = False
                break
        if flag:
            optionPayoff = max(stockPrice - strikePrice, 0)
        else:
            optionPayoff = 0
        totalPayoff += optionPayoff
    return totalPayoff / I / math.exp(r * T)

def testBarrierDownOutCall():
    for i in range(70, 170, 10):
        print(str(i)+"&",end="")
        for j in range(75, 125, 10):
            print(str(round(barrier_down_out_call(100, i, j, 1, 0.05, 0.25),10))+'&', end="")
        print()

def control_variate_underlying_assets_down_out_call(S, strikePrice, barrier, T, r, sigma):
    # parameters
    I = 1000000;   n = 1000;    dt = T / n;     S0 = S
    barrier = barrier * math.exp(0.5826 * sigma * dt ** 0.5)
    optionPayoffs = []
    stockPrices = []
    # pilot simulation
    for i in range(0, I//100):
        stockPrice = S0 + 1 - 1
        flag = True
        for j in range(0, n):
            z = random.normalvariate(0, 1)
            stockPrice = stockPrice*math.exp((r-sigma**2/2)*dt+sigma*dt**0.5*z)
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
    totalPayoff = 0
    ST = S0 * math.exp(r * T)
    for i in range(0, I):
        stockPrice = S0 + 1 - 1
        flag = True
        for j in range(0, n):
            z = random.normalvariate(0, 1)
            stockPrice = stockPrice*math.exp((r-sigma**2/2)*dt+sigma*dt**0.5*z)
            if stockPrice < barrier:
                flag = False
        if flag:
            totalPayoff += max(stockPrice - strikePrice, 0)
        totalPayoff -= lambdaStar * (stockPrice - ST)
    optionPremium = (totalPayoff / I) / math.exp(r * T)
    return optionPremium
