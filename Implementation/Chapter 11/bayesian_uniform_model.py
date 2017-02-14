import pandas_datareader.data as web
import pandas as pd
import numpy as np
import pymc3 as pm

symbols = ['ADS.DE', 'ALV.DE', 'BAS.DE', 'BAYN.DE', 'BEI.DE',
    'BMW.DE', 'CBK.DE', 'CON.DE', 'DAI.DE', 'DB1.DE',
    'DBK.DE', 'DPW.DE', 'DTE.DE', 'EOAN.DE', 'FME.DE',
    'FRE.DE', 'HEI.DE', 'HEN3.DE', 'IFX.DE', 'LHA.DE',
    'LIN.DE', 'LXS.DE', 'MRK.DE', 'MUV2.DE', 'RWE.DE',
    'SAP.DE', 'SDF.DE', 'SIE.DE', 'TKA.DE', 'VOW3.DE',
    '^GDAXI']
data = pd.DataFrame()
for sym in symbols:
    data[sym] = web.DataReader(sym, data_source='yahoo')['Close']
data = data.dropna()
dax = pd.DataFrame(data.pop('^GDAXI'))

model_randomwalk = pm.Model()
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

