import csv
import numpy as np

symbols = ['AAPL', 'MSFT', 'YHOO', 'DB', 'GLD']
noOfAsset = len(symbols)

def readDataFromCSV(filename):
    infile = open(filename, newline = '')
    reader = csv.reader(infile)

    dates = [];    AAPL = [];    MSFT = []
    DB = [];    YHOO = [];    GLD = []
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

def readDataFromCSV(filename, noa):
    infile = open(filename, newline = '')
    reader = csv.reader(infile)

    dates = []
    stocks = [[] for x in range(noa)];
    for row in reader:
        if row[0] != "Date":
            dates.append(row[0])
            for index in range(noa):
                stocks[index].append(float(row[index+1]))

    infile.close()
    return stocks

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

returnData, returnMean = calculateReturnData(readDataFromCSV("Close Prices Data.csv", 5))

weights = np.random.random(noOfAsset)
weights /= np.sum(weights)
meanReturn = np.sum(returnMean * weights) * 252
covMatrix = np.cov(returnData,bias=True)
portfolioVar=np.dot(weights.T,np.dot(covMatrix,weights))*252
portfolioSD = np.sqrt(portfolioVar)
