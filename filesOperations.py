import numpy as np

#procedure for saving results to text files
#besides results, also user specified parameters and run times are stored
def resultsToFile (w, T, assets, fval, alg, params, status, fileName):
    ww = np.round_(100*w.reshape( (T, assets) ), decimals = 4)

    with open(fileName, 'w') as f:
        f.write ('Algorithm: ' + alg + '\n')
        f.write ('Parameters ' + str(params) + '\n\n')
        f.write ('Weights: \n')            
        for i in range(0, T): f.write('T = ' + str(i+1) + ': ' + str(ww[i]) + ' | sum(w) = ' + str(sum(ww[i])) +'\n')        
        f.write('\nObjective function value: ' + str(fval) + '\n\n')
        f.write('Solver output info: ' + str(status))

        if alg == 'QPU':
            total_time = status['timing']['qpu_access_time'] + status['timing']['qpu_access_overhead_time'] + status['timing']['total_post_processing_time']
            f.write ('\n\nTotal run time on QPU: ' + str(total_time/1000) + ' ms')
        elif (alg == 'Hybrid') or (alg == 'Hybrid_Constrained'):
            total_time = status['qpu_access_time']
            f.write ('\n\nTotal run time on QPU: ' + str(total_time/1000) + ' ms\n')
            total_time = status['run_time']
            f.write ('Total run time: ' + str(total_time/1000) + ' ms')

        f.close()