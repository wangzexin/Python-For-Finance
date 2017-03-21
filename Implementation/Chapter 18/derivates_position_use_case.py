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
print(am_put_pos.get_info())
