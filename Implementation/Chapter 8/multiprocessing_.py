import multiprocessing as mp
import math

def simulate_gbm(p):
    M, I = p
    S0 = 100
    r = 0.05
    sigma = 0.2
    T = 1.0
    dt = T / M
    paths = np.zeros((M + 1, I))
    paths[0] = S0
    for t in range(1, M + 1):
        paths[t] = paths[t-1] * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * math.sqrt(dt) * np.random.standard_normal(I))
    return paths

I = 100
M = 100
t = 100

#running on server with 8 cores/16 threads
from time import time
times = []
for w in range(1, 17):
    t0 = time()
    pool = mp.Pool(processes = w)
    result = pool.map(simulate_gbm, t * [(M, I), ])
    times.append(time() - t0)
