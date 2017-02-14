import numpy as np
import numpy.random as npr

def simulate_jump_diffusion(r=.05, sigma=.2, lamb=.75, mu=-.6, delta=.25):
    M = 50;    I = 10000;    T = 1.0;     dt = T / M
    rj = lamb * (np.exp(mu + 0.5 * delta ** 2) - 1)
    S = np.zeros((M + 1, I))
    S0=100;    S[0] = S0
    sn1 = npr.standard_normal((M + 1, I))
    sn2 = npr.standard_normal((M + 1, I))
    poi = npr.poisson(lamb * dt, (M + 1, I))
    for t in range(1, M + 1, 1):
        S[t] = S[t - 1]*(np.exp((r-rj-0.5*sigma**2)*dt
            + sigma * np.sqrt(dt) * sn1[t])
            + (np.exp(mu + delta * sn2[t]) - 1) * poi[t])
        S[t] = np.maximum(S[t], 0)
    return S
