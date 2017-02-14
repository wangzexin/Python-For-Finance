import numpy as np
import numpy.random as npr
import scipy.stats as scs

def gen_paths(S0 = 100, r = .05, sigma = .25, T = 1.0, M = 50, I = 10000):
    ''' Generates Monte Carlo paths for geometric Brownian motion.
    Parameters
    ==========
    S0 : float
    initial stock/index value
    r : float
    constant short rate
    sigma : float
    constant volatility
    T : float
    final time horizon
    M : int
    number of time steps/intervals
    I : int
    number of paths to be simulated
    Returns
    =======
    paths : ndarray, shape (M + 1, I)
    simulated paths given the parameters
    '''
    dt = float(T) / M
    paths = np.zeros((M + 1, I), np.float64)
    paths[0] = S0
    for t in range(1, M + 1):
        rand = np.random.standard_normal(I)
        rand = (rand - rand.mean()) / rand.std()
        paths[t] = paths[t - 1] * np.exp((r - 0.5 * sigma ** 2) * dt +
                                         sigma * np.sqrt(dt) * rand)
    return paths

def normality_tests(arr):
    ''' Tests for normality distribution of given data set.
    Parameters
    ==========
    array: ndarray
    object to generate statistics on
    '''
    print("Skew of data set %14.3f" % scs.skew(arr))
    print("Skew test p-value %14.3f" % scs.skewtest(arr)[1])
    print("Kurt of data set %14.3f" % scs.kurtosis(arr))
    print("Kurt test p-value %14.3f" % scs.kurtosistest(arr)[1])
    print("Norm test p-value %14.3f" % scs.normaltest(arr)[1])
