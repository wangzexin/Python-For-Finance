import numpy as np
import numpy.random as npr

def stochastic_volatility():
    # Parameters
    S0 = 100;    r = 0.05;    v0 = 0.1;
    kappa = 3.0;    theta = 0.25;    sigma = 0.1;    rho = 0.6
    T = 1.0;    M = 50;    I = 10000
    
    #Cholesky decomposition of correlation matrix
    corr_mat = np.zeros((2,2))
    corr_mat[0, :] = [1.0, rho]
    corr_mat[1, :] = [rho, 1.0]
    cho_mat = np.linalg.cholesky(corr_mat)
    
    ran_num = npr.standard_normal((2, M + 1, I))

    v = np.zeros_like(ran_num[0]);    vh = np.zeros_like(v)
    v[0] = v0;    vh[0] = v0; dt = T / M
    for t in range(1, M + 1): # simulation of volatility process
        ran = np.dot(cho_mat, ran_num[:, t, :]) # ensure certain correlation
        vh[t]=(vh[t-1]+kappa*(theta-np.maximum(vh[t-1],0))*dt\
               +sigma*np.sqrt(np.maximum(vh[t-1],0))*np.sqrt(dt)*ran[1])
    v = np.maximum(vh, 0)

    S = np.zeros_like(ran_num[0]);    S[0] = S0
    for t in range(1, M + 1): # simulation of stock prices
        ran = np.dot(cho_mat, ran_num[:, t, :]) # ensure certain correlation
        S[t] = S[t-1] * np.exp((r-0.5 * v[t]) * dt + np.sqrt(v[t]) * ran[0] * np.sqrt(dt))
    
