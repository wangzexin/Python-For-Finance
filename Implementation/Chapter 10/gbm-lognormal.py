def bsm_mcs_valuation(strike):
    ''' Dynamic Black-Scholes-Merton Monte Carlo estimator
        for stock prices.
        Parameters
        ==========
        strike : float
        strike price of the option
        Results
        =======
        value : float
        estimate for present value of call option
    '''
    import numpy as np
    import numpy.random as npr
    S0 = 100.; T = 1.0; r = 0.05; sigma = 0.2
    I = 20000
    value = S0 * npr.lognormal((r - 0.5 * sigma ** 2) * T, sigma * np.sqrt(T), size = I)
    return value
