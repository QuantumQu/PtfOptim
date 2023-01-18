from neal import SimulatedAnnealingSampler

#run simulated annealing "iters" times and pick up the best solution
#it is also possible to set inverse of the Boltzman constant
def advancedSA (quadProg, iters, boltzman):
    fval_best = 1e100
    sampler = SimulatedAnnealingSampler()
    sampler.properties['beta'] = boltzman

    for i in range(0,iters):
        response = sampler.sample(quadProg) 
        f = response.first.energy

        if f < fval_best:
            fval_best = f
            response_best = response
    
    return response_best