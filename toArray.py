import numpy as np

#auxiliary tools for converting dictionaries to arrays
def resultsToArray (dct):
    n = len(dct)
    results = np.zeros( (1,n) )
    for i in range(0,n):
        results[0,i] = dct[i]
    return results[0]

def dictToArray (dct):
    n = len(dct)
    results = np.zeros( (1,n) )
    for i in range(0,n):
        results[0,i] = dct['x_' + str(i)]
    return results[0]