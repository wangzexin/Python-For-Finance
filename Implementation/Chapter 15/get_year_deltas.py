import numpy as np
import datetime as dt

def get_year_deltas(date_list, day_count=365.):
    ''' Return vector of floats with day deltas in years.
    Parameters
    ==========
    date_list : list or array of datetime objects
    day_count : float number of days for a year
        (to account for different conventions)
    delta_list : array of year fractions
    '''
    start = date_list[0]
    delta_list = [(date - start).days / day_count
                  for date in date_list]
    return np.array(delta_list)
