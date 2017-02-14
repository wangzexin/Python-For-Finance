
from math import *
import numpy as np
import numexpr as ne

def perf_comp_data(func_list, data_list, rep=3, number=1):
    ''' the convenience function for comparing performance systematically '''
    from timeit import repeat
    res_list = {}
    for name in enumerate(func_list):
        # enumerate basically create an array of tuples of (index, element)
        stmt = name[1] + '(' + data_list[name[0]] + ')' # function_name(data_name)
        setup = "from __main__ import " + name[1] + ', ' + data_list[name[0]]
        #from __main__ import function_name, data_name
        results = repeat(stmt=stmt, setup=setup, repeat=rep, number=number)
        res_list[name[1]] = sum(results) / rep #take average running time
    res_sort = sorted(res_list.items(), key = lambda x : (x[1],x[0]))
    for item in res_sort:
        rel = item[1] / res_sort[0][1]
        print('function: ' + item[0] + ', av. time sec: %9.5f, ' % item[1]\
              + 'relative: %6.1f' % rel) #C-like print formatting

def f(x):
    return abs(cos(x)) ** 0.5 + sin(2 + 3 * x)

def standard_explicit(a):
    res = []
    for x in a:
        res.append(f(x))
    return res

def iterator_implicit(a):
    return [f(x) for x in a]

def iterator_implicit_eval(a):
    expression = 'abs(cos(x)) ** 0.5 + sin(2 + 3 * x)'
    return [eval(expression) for x in a]

def numpy_vectorized(a):
    a_np = np.arange(len(a))
    return (np.abs(np.cos(a_np)) ** 0.5 + np.sin(2 + 3 * a_np))

def single_threaded(a):
    ex = 'abs(cos(a)) ** 0.5 + sin(2 + 3 * a)'
    ne.set_num_threads(16)
    return ne.evaluate(ex)

def multithreaded_numexpr(a):
    import numexpr as ne
    ex = 'abs(cos(a)) ** 0.5 + sin(2 + 3 * a)'
    ne.set_num_threads(16)
    return ne.evaluate(ex)

a = range(500000)

f1 = standard_explicit
f2 = iterator_implicit
f3 = iterator_implicit_eval
f4 = numpy_vectorized
f5 = single_threaded
f6 = multithreaded
r1 = f1(a)
r2 = f2(a)
r3 = f3(a)
r4 = f4(a)
r5 = f5(a)
r6 = f6(a)

np.allclose(r1, r2)
np.allclose(r1, r3)
np.allclose(r1, r4)
np.allclose(r1, r5)
np.allclose(r1, r6)

func_list = ['f1', 'f2', 'f3', 'f4', 'f5', 'f6']
data_list = ['a', 'a', 'a', 'a', 'a', 'a']
perf_comp_data(func_list, data_list)

'''
function: f4, av. time sec:   0.03077, relative:    1.0
function: f6, av. time sec:   0.08825, relative:    2.9
function: f5, av. time sec:   0.09008, relative:    2.9
function: f2, av. time sec:   0.43923, relative:   14.3
function: f1, av. time sec:   0.48788, relative:   15.9
function: f3, av. time sec:  11.21599, relative:  364.5
>>> np.allclose(r1, r2)
True
>>> np.allclose(r1, r3)
True
>>> np.allclose(r1, r4)
True
>>> np.allclose(r1, r5)
True
>>> np.allclose(r1, r6)
True
>>> 
'''
