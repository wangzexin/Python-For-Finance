import pymc3 as pm
import numpy as np

model_randomwalk = pm.Model()
with model_randomwalk:
    # std of random walk best sampled in log space
    sigma_alpha = pm.Exponential('sigma', 1./.02, testval = .1)
    sigma_beta = pm.Exponential('sigma', 1./.02, testval = .1)
