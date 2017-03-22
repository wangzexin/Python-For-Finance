from dx import *

me_gbm = market_environment("me_gbm", dt.datetime(2015, 1, 1))
me_gbm.add_constant("initial_value", 36.)
me_gbm.add_constant("volatility", 0.2)
me_gbm.add_constant("currency", "EUR")

me_gbm.add_constant("model", "gbm")

from derivatives_position import derivatives_position
me_am_put = market_environment("me_am_put", dt.datetime(2015, 1, 1))
me_am_put.add_constant("maturity", dt.datetime(2015, 12, 31))
me_am_put.add_constant("strike", 40.)
me_am_put.add_constant("currency", "EUR")
payoff_func = "np.maximum(strike - instrument_values, 0)"
am_put_pos = derivatives_position(
    name="am_put_pos",
    quantity=3,
    underlying="gbm",
    mar_env=me_am_put,
    otype="American",
    payoff_func=payoff_func)
am_put_pos.get_info()

me_jd = market_environment('me_jd', me_gbm.pricing_date)
# add jump diffusion-specific parameters
me_jd.add_constant('lambda', 0.3)
me_jd.add_constant('mu', -0.75)
me_jd.add_constant('delta', 0.1)
# add other parameters from gbm
me_jd.add_environment(me_gbm)
# needed for portfolio valuation
me_jd.add_constant('model', 'jd')

me_eur_call = market_environment('me_eur_call', me_jd.pricing_date)
me_eur_call.add_constant('maturity', dt.datetime(2015, 6, 30))
me_eur_call.add_constant('strike', 38.)
me_eur_call.add_constant('currency', 'EUR')
payoff_func = 'np.maximum(maturity_value - strike, 0)'
eur_call_pos = derivatives_position(
    name='eur_call_pos',
    quantity=5,
    underlying='jd',
    mar_env=me_eur_call,
    otype='European',
    payoff_func=payoff_func)

underlyings = {'gbm': me_gbm, 'jd' : me_jd}
positions = {'am_put_pos' : am_put_pos, 'eur_call_pos' : eur_call_pos}

# discounting object for the valuation
csr = constant_short_rate('csr', 0.06)
val_env = market_environment('general', me_gbm.pricing_date)
val_env.add_constant('frequency', 'W')
# monthly frequency
val_env.add_constant('paths', 25000)
val_env.add_constant('starting_date', val_env.pricing_date)
val_env.add_constant('final_date', val_env.pricing_date)
# not yet known; take pricing_date temporarily
val_env.add_curve('discount_curve', csr)
# select single discount_curve for whole portfolio

from derivatives_portfolio import derivatives_portfolio
portfolio = derivatives_portfolio(
    name='portfolio',
    positions=positions,
    val_env=val_env,
    assets=underlyings,
    fixed_seed=True)

print(portfolio.get_statistics())

print(portfolio.get_statistics()[['pos_value', 'pos_delta', 'pos_vega']].sum())

print(portfolio.get_positions())

print(portfolio.valuation_objects['am_put_pos'].present_value())

print(portfolio.valuation_objects['eur_call_pos'].delta())


path_no = 777
path_gbm = portfolio.underlying_objects['gbm'].get_instrument_values()[
    :, path_no]
path_jd = portfolio.underlying_objects['jd'].get_instrument_values()[
    :, path_no]

correlations = [['gbm', 'jd', 0.9]]

port_corr = derivatives_portfolio(
    name='portfolio',
    positions=positions,
    val_env=val_env,
    assets=underlyings,
    correlations=correlations,
    fixed_seed=True)

print(port_corr.get_statistics())

path_gbm = port_corr.underlying_objects['gbm'].\
    get_instrument_values()[:, path_no]
path_jd = port_corr.underlying_objects['jd'].\
    get_instrument_values()[:, path_no]

pv1 = 5 * port_corr.valuation_objects['eur_call_pos'].\
    present_value(full=True)[1]

pv2 = 3 * port_corr.valuation_objects['am_put_pos'].\
    present_value(full=True)[1]

pvs = pv1 + pv2

print(pvs.std())

pv1 = 5 * portfolio.valuation_objects['eur_call_pos'].\
    present_value(full=True)[1]
pv2 = 3 * portfolio.valuation_objects['am_put_pos'].\
    present_value(full=True)[1]

print((pv1 + pv2).std())
