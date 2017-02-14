#import warnings
#warnings.simplefilter('ignore')
import pymc3 as pm
import numpy as np
np.random.seed(1000)

x = np.linspace(0, 10, 500)
y = 4 + 2 * x + np.random.standard_normal(len(x)) * 2

reg = np.polyfit(x, y, 1)

with pm.Model() as model:
    # model specifications in PyMC3
    # are wrapped in a with statement
    # define priors
    alpha = pm.Normal('alpha', mu=0, sd=20)
    beta = pm.Normal('beta', mu=0, sd=20)
    sigma = pm.Uniform('sigma', lower=0, upper=10)
    # define linear regression
    y_est = alpha + beta * x
    # define likelihood
    likelihood = pm.Normal('y', mu=y_est, sd=sigma, observed=y)
    # inference
    #start = pm.find_MAP()
    # find starting value by optimization
    #step = pm.NUTS(state=start)
    # instantiate MCMC sampling algorithm
    #trace = pm.sample(100, step, start=start, progressbar=False)
    # draw 100 posterior samples using NUTS sampling

model_randomwalk = pm.Model()
with model_randomwalk:
    # std of random walk best sampled in log space
    sigma_alpha, log_sigma_alpha = \
        model_randomwalk.TransformedVar('sigma_alpha',
        pm.Exponential.dist(1. / .02, testval=.1),
        pm.logtransform)
    sigma_beta, log_sigma_beta = \
        model_randomwalk.TransformedVar('sigma_beta',
        pm.Exponential.dist(1. / .02, testval=.1),
        pm.logtransform)

