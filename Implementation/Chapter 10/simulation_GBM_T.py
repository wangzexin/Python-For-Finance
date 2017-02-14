def simulate_geometric_brownian_motion_T():
    import numpy as np
    import numpy.random as npr
    S0 = 100 # initial value
    r = 0.05 # constant short rate
    sigma = 0.25 # constant volatility
    T = 2.0 # in years
    I = 10000
    ST1 = S0 * np.exp((r-0.5*sigma**2)*T+sigma*np.sqrt(T)*npr.standard_normal(I))
    ST2 = S0 * npr.lognormal((r-0.5*sigma**2)*T, sigma*np.sqrt(T), size = I)
