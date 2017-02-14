import numpy as np
from math import *

def binomial_np(strike):
  # assumptions
  M = 1000
  S0 = 100
  T = 1. # call option maturity
  r = 0.05 # constant short rate
  vola = 0.20 # constant volatility factor
  dt = T / M
  df = exp(-r * dt)
  u = exp(vola * sqrt(dt))
  d = 1 / u
  q = (exp(r * dt) - d) / (u - d) # risk neutral probability
  mu = np.arange(M+1)
  mu = np.resize(mu, (M+1, M+1))
  md = np.transpose(mu)
  mu = u ** (mu - md)
  md = d ** md
  S = S0 * mu * md
  pv = np.maximum(S - strike, 0)
  z = 0
  for t in range(M-1, -1, -1):
    pv[0:M-z, t] = (q * pv[0:M-z, t+1] + (1-q) * pv[1:M-z+1, t+1]) * df
    z += 1
  return pv[0,0]

def binomial_py(strike):
    S0 = 100; r = 0.05 # constant short rate
    T = 1. # call option maturity
    vola = 0.20 # constant volatility factor
    M = 1000; dt = T / M;  df = exp(-r * dt) # time parameters
    u = exp(vola * sqrt(dt));  d = 1 / u # binomial parameters
    q = (exp(r * dt) - d) / (u - d) # risk neutral probability
    S = np.zeros((M+1, M+1), dtype = np.float64)
    S[0,0] = S0;  z1 = 0
    for j in range(1, M+1, 1): #future stock pricings
      z1 += 1
      for i in range(z1 + 1):
        S[i,j] = S[0,0] * (u ** j) * (d ** (i*2))
    iv = np.zeros((M+1, M+1), dtype = np.float64)
    z2 = 0
    for j in range(0, M+1, 1): #future call option pricings
      for i in range(z2 + 1):
        iv[i, j] = max(S[i,j]-strike, 0)
      z2 += 1
    pv = np.zeros((M+1, M+1), dtype = np.float64)
    pv[:, M] = iv[:, M];  z3 = M+1
    for j in range(M-1, -1, -1):
      z3 -= 1
      for i in range(z3):
        pv[i,j] = (q * pv[i, j+1] + (1-q) * pv[i+1, j+1]) * df
    return pv[0,0]
