import math
import numpy as np
import scipy.linalg as scl

def crankNicolsonCall(S, K, T, r, sigma):
    M = 1000
    N = 1000
    dt = T / N
    ds = 2 * S / M
    sVector = [x * ds for x in range(M+10)]
    tVector = [x * dt for x in range(N+10)]
    alpha = [0.25*dt*(sigma**2*i**2-r*i) for i in range(M+1)]
    beta = [-0.5*dt*(sigma**2*i**2+r) for i in range(M+1)]
    gamma = [0.25*dt*(sigma**2*i**2+r*i) for i in range(M+1)]
    C = [[0 for x in range(M-1)] for y in range(M-1)]
    D = [[0 for x in range(M-1)] for y in range(M-1)]
    for i in range(M-1):
        C[i][i] = 1 - beta[2+i]
        D[i][i] = 1 + beta[2+i]
    for i in range(1, M-1, 1):
        C[i-1][i] = -gamma[1+i]
        D[i-1][i] = gamma[1+i]
        C[i][i-1] = -alpha[2+i]
        D[i][i-1] = alpha[2+i]
    Cmatrix = np.asmatrix(C)
    Dmatrix = np.asmatrix(D)
    priceEnd = [0 for x in range(N+1)]
    for i in range(N+1):
        priceEnd[i] = (2*S - K) * math.exp(-r*(N-i)*dt)
    price = [0 for x in range(M-1)]
    for i in range(M-1): # boundary condition for V_i,N for all i
        price[i] = max(sVector[i+1] - K, 0)
    priceV = np.transpose(np.asmatrix(price)) # shape: M-1, 1
    offset = [[0] for x in range(M-1)] # shape: M-1, 1
    invC = scl.inv(C)
    for i in range(N):
        offset[M-2][0] = gamma[M] * (priceEnd[i] + priceEnd[i+1])
        offsetV = np.asmatrix(offset) # shape: M-1, 1
        temp = np.dot(Dmatrix, priceV) # shape: M-1, 1
        temp = temp + offsetV # shape: M-1, 1
        temp = np.dot(invC, temp) # shape: M-1, 1
        priceV = temp # shape: M-1, 1
    return priceV[M//2]

def testCall():
    for i in range(105, 205, 5):
        print(i,"&",float(crankNicolsonCall(100, i, 1, 0.05, 0.25)),'&')

def crankNicolsonPut(S, K, T, r, sigma):
    M = 1000
    N = 1000
    dt = T / N
    ds = 2 * S / M
    sVector = [x * ds for x in range(M+10)]
    tVector = [x * dt for x in range(N+10)]
    alpha = [0.25*dt*(sigma**2*i**2-r*i) for i in range(M+1)]
    beta = [-0.5*dt*(sigma**2*i**2+r) for i in range(M+1)]
    gamma = [0.25*dt*(sigma**2*i**2+r*i) for i in range(M+1)]
    C = [[0 for x in range(M-1)] for y in range(M-1)]
    D = [[0 for x in range(M-1)] for y in range(M-1)]
    for i in range(M-1):
        C[i][i] = 1 - beta[2+i]
        D[i][i] = 1 + beta[2+i]
    for i in range(1, M-1, 1):
        C[i-1][i] = -gamma[1+i]
        D[i-1][i] = gamma[1+i]
        C[i][i-1] = -alpha[2+i]
        D[i][i-1] = alpha[2+i]
    Cmatrix = np.asmatrix(C)
    Dmatrix = np.asmatrix(D)
    priceStart = [0 for x in range(N+1)]
    for i in range(N+1):
        priceStart[i] = (K) * math.exp(-r*(N-i)*dt)
    price = [0 for x in range(M-1)]
    for i in range(M-1): # boundary condition for V_i,N for all i
        price[i] = max(K - sVector[i+1], 0)
    priceV = np.transpose(np.asmatrix(price)) # shape: M-1, 1
    offset = [[0] for x in range(M-1)] # shape: M-1, 1
    invC = scl.inv(C)
    for i in range(N-1,-1,-1):
        offset[M-2][0] = alpha[2] * (priceStart[i] + priceStart[i+1])
        offsetV = np.asmatrix(offset) # shape: M-1, 1
        temp = np.dot(Dmatrix, priceV) # shape: M-1, 1
        temp = temp + offsetV # shape: M-1, 1
        temp = np.dot(invC, temp) # shape: M-1, 1
        priceV = temp # shape: M-1, 1
    return priceV[M//2]

def testPut():
    for i in range(105, 205, 5):
        print(i,"&",float(crankNicolsonPut(100, i, 1, 0.05, 0.25)),'&')
