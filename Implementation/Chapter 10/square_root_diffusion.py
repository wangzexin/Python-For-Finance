def square_root_diffusion():
    x0 = 0.05; kappa = 3.0; theta = 0.02; sigma = 0.1 # model parameters
    I = 10000; M = 50; T = 1; dt = T / M # time parameters
    xh = np.zeros((M+1, I)); x1 = np.zeros_like(xh)
    xh[0] = x0; x1[0] = x0
    for t in range(1, M+1):
        xh[t] = (xh[t-1]+kappa*(theta-np.maximum(xh[t-1],0))*dt\
          +sigma*np.sqrt(np.maximum(xh[t-1],0))*np.sqrt(dt)*npr.standard_normal(I))
    x1 = np.maximum(xh, 0)
    return x1
