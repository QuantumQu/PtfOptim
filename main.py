#Markowitz-like dynamic portfolio optimization with discrete time, sovled by QUBO approach with D-Wave quantum annealer

from os import system #allows to clear the console output
#---------------------------------------------------------------------------------
import ptfOptim as ptf #my function for the actual ptf optimization
import inputData as dt #input data for the optimization
import filesOperations as fl #interaction with files
#---------------------------------------------------------------------------------
    
#load covariance matrices, returns and transaction costs (stored in module inputData)
[C, r, V] = dt.loadData('ActualToy') 

binVars = 3 #asset weight accuracy

riskAversion = 10 #generally known as lambda in Markowitz model
costSensitivity = 20 #importance of transaction costs
constraintForce = 10 #importance of constraint sum(w) = 1 for each time period

#comment/uncomment solver you want to use
params = {} #default parameters - empty dict, only SA and QPU need parameters to be specified

#simulated annealing
#alg = 'SA'
#params = {'iter': 100, 'boltzman': 1}

#QPU (basics settings, only number of reads is set)
#alg = 'QPU_Default'
#params = {'num_reads': 1000} 

#QPU (with detailed settings, see below)
alg = 'QPU'
#num_reads - number of repetitions, annealing_time - length of annealing cyclus in microsecs (default: 20)
#chain_strength - an importance of preserving value consitency among physical qubits representing one logical qubit, the strength should be close to maximal coef. in the objective function
#readout_thermalization - number of microseconds waiting before reading results to cool the QPU down and restrict a noise
params = {'num_reads': 50,'chain_strength': constraintForce,'readout_thermalization': 10, 'annealing_time': 20} 

#exact sovler !!!10 variables at maximum!!!!
#alg = 'Exact' 

#hybrid sovler with sum(w) = 1 constraint in penalty function
#alg = 'Hybrid'

#hybrid sovler with sum(w) = 1 constraint specified with class Hybrid Constrained Model
#alg = 'Hybrid_Constrained'

system('clear') #clear console
print('Working...')

maxIter = 10 #number of repetion of the calculation

#results are stored in folder/file named alg + '_results/results_' + iterNumber + '.txt'

for i in range(0,maxIter):
    print('Iter ' + str(i))

    if alg == 'Hybrid_Constrained':
        [w, f, status] = ptf.solvePtfOptimTaskConstrained(C, r, V, riskAversion, costSensitivity, constraintForce, binVars)
    else:
        [w, f, status] = ptf.solvePtfOptimTask(C, r, V, riskAversion, costSensitivity, constraintForce, binVars, alg, params)

    fl.resultsToFile(w, len(C), len(r[0]), f, alg, params, status, alg + '_results/results_' + str(i+1) + '.txt')

print('Finished!')