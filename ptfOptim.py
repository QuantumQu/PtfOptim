#procedures for preparing QUBO task describing portfolio optimization
import numpy as np
#--------------------------------------D-Wave---------------------------------------------------
from dimod import Binary, BinaryQuadraticModel, ConstrainedQuadraticModel, ExactSolver
from dwave.system import LeapHybridCQMSampler  
from dwave.system.samplers import DWaveSampler, LeapHybridSampler
from dwave.system.composites import EmbeddingComposite
#--------------------------------------my modules-----------------------------------------------
import toArray as ta #utils for post-processing of returned arrays
import quadProgramBinarization as qpBin #utils for transforming QP to QUBO and its results back to real numbers
import advancedSimAnneal as sa #simulated annealing (allows to repeat the optimization many times and set Boltzman constant)

#prepare objective QUBO version of portfolio optimization 
#matrix A, vector b  and constant c in quadratic objective function function w^T*A*w + b^T*w + c are returned
#A,b,c are based on covariance matrix (C), average returns (r) and transaction costs (V)
def preparePtfOptimTask (C, r, V, lmbd, mu, F, binVars):       
    T = len(C)
    assets = len(r[0])
    vars = T*assets

    VV = V
    VV.append (np.zeros( (assets, assets) ))    

    A = np.zeros( (vars, vars) )
    b = np.zeros( (1, vars) )

    indx = 0
    
    for i in range(0,T):        
        A[indx:(indx + assets),indx:(indx + assets)] = lmbd*C[i] + mu*(VV[i] + VV[i+1]) + F*np.ones( (assets, assets) )
        if i < T-1:
            A[indx:(indx + assets),(indx + assets):(indx + 2*assets)] = -1*mu*VV[i+1]
            A[(indx + assets):(indx + 2*assets),indx:(indx + assets)] = -1*mu*VV[i+1]

        b[0,indx:(indx + assets)] = -1*r[i] - 2*F*np.ones( (1,assets) )

        indx += assets

    const = F*T
    
    [A, b] = qpBin.binarizeQuadProgram (A, b[0], binVars) #binarization
    b = b[0] #b is expected to be a vector
    return [A, b, const]

#same as procedure preparePtfOptimTask but based on ConstrainedQuadraticModel class
def solvePtfOptimTaskConstrained (C, r, V, riskAversion, costSensitivity, constraintForce, binVars):
    T = len(r)
    assets = len(r[0])

    vars = T*assets*binVars

    [A, b, const] = preparePtfOptimTask (C, r, V, riskAversion, costSensitivity, constraintForce, binVars)  

    cqm = ConstrainedQuadraticModel()
    x = [Binary(f'x_{i}')  for i in range(0,vars)]

    indx = 0
    for t in range(0,T):
        w_sum = 0
        for i in range(0,assets):
            for k in range(0, binVars):
                w_sum += 2**(-1*(k+1))*x[indx]
                indx += 1
        cqm.add_constraint(w_sum == 1, label = 'Weights sum, t = ' + str(t+1)) 

    f = 0
    for i in range(0,vars):
        for j in range(0,vars):
            f += x[i]*x[j]*A[i,j]
        f += b[i]*x[i]
    f += const

    cqm.set_objective(f)

    response = LeapHybridCQMSampler().sample_cqm(cqm)
    x_res = ta.dictToArray(response.first.sample)
    return [qpBin.getDecimalWeights (x_res, binVars), response.first.energy, response.info] 

#the procedure call a solver with specified parameters for portfolio optimization defined with covariance matrix (C), average returns (r) and transaction costs (V)
def solvePtfOptimTask (C, r, V, riskAversion, costSensitivity, constraintForce, binVars, alg, params):
    processOptimization = True

    if alg == 'SA':
        if ('iter' not in params.keys()) or ('boltzman' not in params.keys()):
            print('Simulated annealing: Missing parameters boltzman and/or beta.')
            processOptimization = False
    elif alg == 'QPU':
        if ('num_reads' not in params.keys()) or ('annealing_time' not in params.keys()) or ('chain_strength' not in params.keys()) or ('readout_thermalization' not in params.keys()):
            print('QPU: Missing parameter num_reads, annealing_time, readout_thermalization and/or chain_strength.')
            processOptimization = False
    elif alg == 'QPU_Default':
        if ('num_reads' not in params.keys()):
            print('QPU_Default: Missing parameter num_reads.')
            processOptimization = False
    elif (alg != 'Hybrid') and (alg != 'Exact'):
        print('Unknown algorithm')
        processOptimization = False

    if processOptimization:
        [A, b, const] = preparePtfOptimTask (C, r, V, riskAversion, costSensitivity, constraintForce, binVars) 
        bqm = BinaryQuadraticModel(b, A, const, 'BINARY')

        if alg == 'Exact':
            sampler = ExactSolver()
            response = sampler.sample(bqm) 
        elif alg == 'SA':
            response = sa.advancedSA(bqm, iters = params['iter'], boltzman = params['boltzman'])                                
        elif alg == 'Hybrid':
            sampler = LeapHybridSampler()
            response = sampler.sample(bqm) 
        elif alg == 'QPU':
            sampler = DWaveSampler()                        
            response = EmbeddingComposite(sampler).sample(bqm, num_reads=params['num_reads'], annealing_time = params['annealing_time'], chain_strength = params['chain_strength'], readout_thermalization = params['readout_thermalization'])            
        elif alg == 'QPU_Default':
            sampler = DWaveSampler()                        
            response = EmbeddingComposite(sampler).sample(bqm, num_reads=params['num_reads'])            
            
        x = ta.resultsToArray(response.first.sample)
        w = qpBin.getDecimalWeights (x, binVars)
        f = response.first.energy   
        status = response.info 
        return [w, f, status]    
    else:
        return [0, 1e300, 'n/a']
    
