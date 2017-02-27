from dx_simulation import *
me_gbm = market_environment('me_gbm', dt.datetime(2015, 1, 1))
me_gbm.add_constant('initial_value', 36.)
me_gbm.add_constant('volatility', 0.2)
me_gbm.add_constant('final_date', dt.datetime(2016, 12, 31))
me_gbm.add_constant('currency', 'EUR')
me_gbm.add_constant('frequency', 'W')
# weekly frequency
me_gbm.add_constant('paths', 50000)
csr = constant_short_rate('csr', 0.06)
me_gbm.add_curve('discount_curve', csr)
gbm = geometric_brownian_motion('gbm', me_gbm)

payoff_func = 'np.maximum(strike - instrument_values, 0)'

me_am_put = market_environment('me_am_put', dt.datetime(2015, 1, 1))
me_am_put.add_constant('maturity', dt.datetime(2015, 12, 31))
me_am_put.add_constant('strike', 40.)
me_am_put.add_constant('currency', 'EUR')

from valuation_mcs_american import valuation_mcs_american
am_put = valuation_mcs_american('am_put', underlying=gbm,
                                mar_env=me_am_put, payoff_func=payoff_func)
am_put.present_value(fixed_seed=True, bf=5)
ls_table = []
for initial_value in (36., 38., 40., 42., 44.):
    for volatility in (0.2, 0.4):
        for maturity in (dt.datetime(2015, 12, 31),
                            dt.datetime(2016, 12, 31)):
            am_put.update(initial_value=initial_value,
                    volatility=volatility,
                    maturity=maturity)
            ls_table.append([initial_value,
                    volatility,
                    maturity,
                    am_put.present_value(bf=5)])

print("S0 | Vola | T | Value")
print(22 * "-")
for r in ls_table:
    print("%d | %3.1f | %d | %5.3f" % (r[0], r[1], r[2].year - 2014, r[3]))

