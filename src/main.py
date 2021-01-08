import parser
from mutation import mutation
from crossover import crossover
from select import select
from objectivefunc import stop_condition
from init import createInitPopulation
from settings import MI, CROSSOVER_PROB, K, LAMBDA, save


import random
import json
import os
from varname import nameof

if __name__ == 'main':
    populations = []
    populations.append(createInitPopulation(MI)) # MI elements
    t = 0
    stop = False
    while not stop:
        temporary_population = []
        for i in range(LAMBDA):
            a = random.uniform(0, 1)
            if a < CROSSOVER_PROB:
                temporary_population.append(mutation(crossover(select(populations[t], K))))
            else:
                temporary_population.append(mutation(select(populations[t], 1)))
        populations.append(temporary_population)
        if stop_condition(populations[t], t):
            stop = True
        t += 1
    
    # SAVE
    save(populations)