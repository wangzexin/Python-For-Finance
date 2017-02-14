import csv
import numpy as np

def readDataFromCSV(filename):
    infile = open(filename, newline = '')
    reader = csv.reader(infile)

    dates = []
    AAPL = []
    MSFT = []
    DB = []
    YHOO = []
    GLD = []
    for row in reader:
        if row[0] != "Date":
            dates.append(row[0])
            AAPL.append(float(row[1]))
            MSFT.append(float(row[2]))
            DB.append(float(row[3]))
            YHOO.append(float(row[4]))
            GLD.append(float(row[5]))

    infile.close()

    return [AAPL, MSFT, DB, YHOO, GLD]

def calculateReturnData(dataset):
    for stock in dataset:
        stock.reverse()
    returnData = []
    returnMean = []
    for stock in dataset:
        returns = []
        for i in range(1,len(stock)):
            returns.append(stock[i] / stock[i-1] - 1)
        returnData.append(returns)
        returnMean.append(np.mean(returns))
    returnData = np.array(returnData, np.float64)
    returnMean = np.array(returnMean, np.float64)
    return returnData, returnMean

def generate_statistics(rets, retsMean):
    def statistics(weights):
        ''' Returns portfolio statistics.
        Parameters
        ==========
        weights : array-like
        weights for different securities in portfolio
        Returns
        =======
        pret : float
        expected portfolio return
        pvol : float
        expected portfolio volatility
        pret / pvol : float
        Sharpe ratio for rf=0
        '''
        weights = np.array(weights)
        pret = np.sum(retsMean * weights) * 252
        pvol = np.sqrt(np.dot(weights.T, np.dot(np.cov(rets, bias=True) * 252, weights)))
        return np.array([pret, pvol, pret / pvol])
    return statistics

returnData, returnMean = calculateReturnData(readDataFromCSV("Close Prices Data.csv"))
stat = generate_statistics(returnData, returnMean)

import scipy.optimize as sco

def portfolio_efficient_frontier(statistics, noa, tret):
    min_func_var = lambda weights : statistics(weights)[1]
    cons = ({'type': 'eq', 'fun': lambda x: statistics(x)[0] - tret},
        {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bnds = tuple((0, 1) for x in range(noa))
    EWP = noa * [1. / noa,]
    return sco.minimize(min_func_var, EWP,
                        method='SLSQP',bounds=bnds, constraints=cons)

def create_efficient_frontier(statistics, noa):
    targetReturns = np.linspace(0.0, 0.25, 50)
    points = []
    for targetReturn in targetReturns:
        opts = portfolio_efficient_frontier(statistics, noa, targetReturn)
        w = opts['x']
        points.append(statistics(w))
    return points
