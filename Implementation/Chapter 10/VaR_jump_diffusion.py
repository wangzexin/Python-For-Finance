import numpy as np
import numpy.random as npr
import scipy.stats as scs

def VaR_jump_diffusion(r=.05, sigma=.2, lamb=.75, mu=-.6, delta=.25):
    M = 50;    I = 10000;    dt = 30. / 365 / M
    rj = lamb * (np.exp(mu + 0.5 * delta ** 2) - 1)
    S = np.zeros((M + 1, I));    S0 = 100;    S[0] = S0
    sn1 = npr.standard_normal((M + 1, I))
    sn2 = npr.standard_normal((M + 1, I))
    poi = npr.poisson(lamb * dt, (M + 1, I))
    for t in range(1, M + 1, 1):
        S[t] = S[t - 1]*(np.exp((r-rj-0.5*sigma**2)*dt
            + sigma * np.sqrt(dt) * sn1[t])
            + (np.exp(mu + delta * sn2[t]) - 1) * poi[t])
        S[t] = np.maximum(S[t], 0)
    R_jd = np.sort(S[-1] - S0)
    percs = [0.01, 0.1, 1., 2.5, 5.0, 10.0]
    var = scs.scoreatpercentile(R_jd, percs)
    print("%16s %16s" % ('Confidence Level', 'Value-at-Risk'))
    print(33 * "-")
    for pair in zip(percs, var):
        print("%16.2f %16.3f" % (100 - pair[0], -pair[1]))
