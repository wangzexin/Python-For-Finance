def gen_sn(M, I, anti_paths=True, mo_match=True):
    ''' Function to generate random numbers for simulation.
    Parameters
    M : int  number of time intervals for discretization
    I : int  number of paths to be simulated
    anti_paths: Boolean  use of antithetic variates
    mo_math : Boolean  use of moment matching'''
    if anti_paths is True: # "is True" is different from == True
        sn = npr.standard_normal((M + 1, I / 2)) # generate half
        sn = np.concatenate((sn, -sn), axis=1) # add negative half
    else:
        sn = npr.standard_normal((M + 1, I))
    if mo_match is True:
        sn = (sn - sn.mean()) / sn.std()
    return sn
