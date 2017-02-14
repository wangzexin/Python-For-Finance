import pandas_datareader.data as web
import pandas as pd
import numpy as np
import pymc3 as pm

symbols = ['GLD', 'GDX']
data = pd.DataFrame()
for sym in symbols:
    data[sym] = web.DataReader(sym, data_source='yahoo')['Close']
data = data.dropna()

#from pymc3.distributions.timeseries import GaussianRandomWalk
# to make the model simpler, we will apply the same coefficients
# to 50 data points at a time
subsample_alpha = 50
subsample_beta = 50
model_randomwalk = pm.Model()
with model_randomwalk:
    # std of random walk best sampled in log space
    sigma_alpha = pm.Exponential('sigma_alpha', 1./.02, testval = .1)
    sigma_beta = pm.Exponential('sigma_beta', 1./.02, testval = .1)

with model_randomwalk:
    alpha = pm.GaussianRandomWalk('alpha', sigma_alpha**-2,
                                  shape= len(data) // subsample_alpha)
    beta = pm.GaussianRandomWalk('beta', sigma_beta**-2,
                                 shape= len(data) // subsample_beta)
    # make coefficients have the same length as prices
    alpha_r = np.repeat(alpha, subsample_alpha)
    beta_r = np.repeat(beta, subsample_beta)

with model_randomwalk:
    # define regression
    regression = alpha_r + beta_r * data.GDX.values[:1950]
    # assume prices are normally distributed
    # the mean comes from the regression
    sd = pm.Uniform('sd', 0, 20)
    likelihood = pm.Normal('GLD',
            mu=regression,
            sd=sd,
            observed=data.GLD.values[:1950])
