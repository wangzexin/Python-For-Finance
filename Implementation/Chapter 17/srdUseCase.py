from dx_simulation import *

me_srd = market_environment('me_srd', dt.datetime(2015, 1, 1))
me_srd.add_constant('initial_value', .25)
me_srd.add_constant('volatility', 0.05)
me_srd.add_constant('final_date', dt.datetime(2015, 12, 31))
me_srd.add_constant('currency', 'EUR')
me_srd.add_constant('frequency', 'W')
me_srd.add_constant('paths', 10000)

# specific to simualation class
me_srd.add_constant('kappa', 4.0)
me_srd.add_constant('theta', 0.2)

# required but not needed for the class
me_srd.add_curve('discount_curve', constant_short_rate('r', 0.0))
from square_root_diffusion import square_root_diffusion
srd = square_root_diffusion('srd', me_srd)

srd_paths = srd.get_instrument_values()[:, :10]

