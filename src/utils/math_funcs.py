from math import *
# this is meant for all the extra math functions

def gaussian_function(x:float, a:float,b:float,c:float)->float:
    """
    The gaussian function.

    https://en.wikipedia.org/wiki/Gaussian_function
    """
    return a * e**-((x-b)**2/(2 * c**2))