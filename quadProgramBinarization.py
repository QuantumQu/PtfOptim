import numpy as np

#procedure for binarization of portfolio optimization task
#real weight w_j is replaced with sum_i (x_ij 2^*(-i)), where x_ij is a binary variable, i is going from 1 to N
#N is accuracy of weight w_j binary interpretation
def binarizeQuadProgram (A, b, el):
    n = len(A)
    n_b = n*el
    
    A_b = np.zeros( (n_b, n_b) )
    b_b = np.zeros( (1, n_b) )
    
    p = np.zeros( (1, el) )    
    
    for i in range(1,el + 1):
        p[0,i-1] = 2**(-i)
    
    Q = np.transpose(p).dot(p)
    
    indx_r = 0
  
    for i in range(0,n):
        indx_c = 0
    
        for j in range(0,n):
            A_b[indx_r:(indx_r + el),indx_c:(indx_c + el)] = A[i,j]*Q      
            
            indx_c += el 
    
        b_b[0][indx_r:(indx_r + el)] = b[i]*p
    
        indx_r += el 
    
    return [A_b, b_b]

#the procedure converts results in form of binary variables back to real weights of assets
def getDecimalWeights(x, binVars):
    el = binVars #renaming the variable (to make the code more succinct)
    n = len(x)//el #// ...integer division
    w = np.zeros( (1, max(n, 3)) )
    p = np.zeros( (1, el) )
    
    for i in range(1,el + 1):
        p[0,i-1] = 2**(-i)
    
    indx = 0
    for i in range(0,n):        
        w[0,i] = p.dot(np.transpose(x[indx:(indx + el)]))
        indx += el
        
    return w[0]