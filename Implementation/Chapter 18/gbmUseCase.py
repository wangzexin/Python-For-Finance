from dx_frame import *

me_gbm = market_environment('me_gbm', dt.datetime(2015, 1, 1))
me_gbm.add_constant('initial_value', 36.)
me_gbm.add_constant('volatility', 0.2)
me_gbm.add_constant('final_date', dt.datetime(2015, 12, 31))
me_gbm.add_constant('currency', 'EUR')
me_gbm.add_constant('frequency', 'M')
# monthly frequency (respective month end)
me_gbm.add_constant('paths', 10000)
csr = constant_short_rate('csr', 0.05)
me_gbm.add_curve('discount_curve', csr)

from dx_simulation import *
gbm = geometric_brownian_motion('gbm', me_gbm)
gbm.generate_time_grid()
paths_1 = gbm.get_instrument_values()
gbm.update(volatility=0.5)
paths_2 = gbm.get_instrument_values()
