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

def convergenceDownOutCall(S, strikePrice, barrier, T, r, sigma):
    # parameters
    I = 500000;   n = 500;    dt = T / n;     S0 = S
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
        if (i+1) % 5000 == 0:
            print((i+1), "&", totalPayoff / (i+1) / math.exp(r * T))
    return totalPayoff / I / math.exp(r * T)

