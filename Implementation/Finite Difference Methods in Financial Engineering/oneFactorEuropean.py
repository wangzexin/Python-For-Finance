import math

def oneFactorEuropeanCall(S, K, T, r, sigma):
    M = 500
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
    for i in range(M+1): # boundary condition for V_i,N for all i
        grid[i][N] = max(sVector[i] - K, 0)
    for i in range(N+1): # boundary condition for V_M,j for all j
        grid[M][i] = (sVector[M] - K) * math.exp(-r * (N-i) * dt)
    for j in range(N, 0, -1):
        for i in range(2, M):
            grid[i][j-1] = alpha[i] * grid[i-1][j] + beta[i] * grid[i][j] + gamma[i] * grid[i+1][j]
    trueS = M//2 * ds
    if trueS > S:
        ratio = (trueS - S) / ds
        return ratio * grid[M//2-1][0] + (1 - ratio) * grid[M//2][0]
    else:
        ratio = (S - trueS) / ds
        return ratio * grid[M//2+1][0] + (1 - ratio) * grid[M//2][0]

def testCall():
    for i in range(105, 205, 5):
        print(i, "&", oneFactorEuropeanCall(100, i, 1, 0.05, 0.25), "&")

def oneFactorEuropeanPut(S, K, T, r, sigma):
    M = 500
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
    for i in range(M+1): # boundary condition for V_i,N for all i
        grid[i][N] = max(K - sVector[i], 0)
    for i in range(N+1): # boundary condition for V_M,j for all j
        grid[M][i] = (K - sVector[M]) * math.exp(-r * (N-i) * dt)
    for j in range(N, 0, -1):
        for i in range(2, M):
            grid[i][j-1] = alpha[i] * grid[i-1][j] + beta[i] * grid[i][j] + gamma[i] * grid[i+1][j]
    trueS = M//2 * ds
    if trueS > S:
        ratio = (trueS - S) / ds
        return ratio * grid[M//2-1][0] + (1 - ratio) * grid[M//2][0]
    else:
        ratio = (S - trueS) / ds
        return ratio * grid[M//2+1][0] + (1 - ratio) * grid[M//2][0]

def testPut():
    for i in range(105, 205, 5):
        print(i, "&", oneFactorEuropeanPut(100, i, 1, 0.05, 0.25), "&")
