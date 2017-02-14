from dx_simulation import *

me_jd = market_environment('me_jd', dt.datetime(2015, 1, 1))
# add jump diffusion specific parameters
me_jd.add_constant('lambda', 0.3)
me_jd.add_constant('mu', -0.75)
me_jd.add_constant('delta', 0.1)
me_jd.add_environment(me_gbm)
from jump_diffusion import jump_diffusion
jd = jump_diffusion('jd', me_jd)
paths_3 = jd.get_instrument_values()
jd.update(lamb=0.9)
paths_4 = jd.get_instrument_values()
