import numpy as np

def oneFactorEuropeanCall(S, K, T, r, sigma):
    M = 10
    dt = 0.9 / (sigma**2 * M**2)
    N = int(T / dt) + 1
    dt = T / N
    ds = 2 * S / M
    sVector = [x * ds for x in range(M+10)]
    tVector = [x * dt for x in range(N+10)]
    alpha = [0.5*dt*(sigma**2*i**2-r*i) for i in range(M+10)]
    beta = [1-dt*(sigma**2*i**2+r) for i in range(M+10)]
    gamma = [0.5*dt*(sigma**2*i**2+r*i) for i in range(M+10)]
    grid = [[0 for y in range(N+10)] for x in range(M+10)]
    for i in range(M): # boundary condition for V_i,N for all i
        grid[i][N] = max(sVector[i] - K, 0)
    for i in range(N): # boundary condition for V_M,j for all j
        grid[M][i] = (sVector[M] - K) * np.exp(-r * (N-i) * dt)
    for j in range(N, 0, -1):
        for i in range(2, M):
            grid[i][j-1] = alpha[i] * grid[i-1][j] + beta[i] * grid[i][j] + gamma[i] * grid[i+1][j]
        grid[M][j-1] = (alpha[M] - beta[M]) * grid[M-1][j] + (beta[M] + 2 * gamma[M]) * grid[M][j]
    print(grid)
    return grid[M//2][1]