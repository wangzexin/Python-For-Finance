from sklearn.decomposition import KernelPCA
import pandas_datareader.data as web
import numpy as np
import pandas as pd

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

scale_function = lambda x: (x - x.mean()) / x.std() # convenience function
get_we = lambda x: x / x.sum() # convenience function
pca = KernelPCA().fit(data.apply(scale_function)) # multiple components

pca = KernelPCA(n_components=1).fit(data.apply(scale_function)) # single component
dax['PCA_1'] = pca.transform(-data)

pca = KernelPCA(n_components=5).fit(data.apply(scale_function)) # five components
pca_components = pca.transform(-data)
weights = get_we(pca.lambdas_)
dax['PCA_5'] = np.dot(pca_components, weights)

cut_date = '2011/7/1'
early_pca = dax[dax.index < cut_date]['PCA_5']
early_reg = np.polyval(np.polyfit(early_pca,
dax['^GDAXI'][dax.index < cut_date], 1),early_pca)

late_pca = dax[dax.index >= cut_date]['PCA_5']
late_reg = np.polyval(np.polyfit(late_pca,
dax['^GDAXI'][dax.index >= cut_date], 1),late_pca)
