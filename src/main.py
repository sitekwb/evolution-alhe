from sndlibparser import nodes, links
from mutation import mutation
from crossover import crossover
from select import select
from objectivefunc import stop_condition
from init import createInitPopulation
from settings import MI, CROSSOVER_PROB, KNEE, LAMBDA, save

import random

if __name__ == 'main':
    populations = []
    populations.append(createInitPopulation(MI)) # MI elements
    t = 0
    while not stop_condition(populations[t], t):
        temporary_population = []
        for i in range(LAMBDA):
            a = random.uniform(0, 1)
            if a < CROSSOVER_PROB:
                temporary_population.append(mutation(crossover(select(populations[t], 2), KNEE)))
            else:
                temporary_population.append(mutation(select(populations[t], 1)))
        populations.append(temporary_population)
        t += 1
    
    # SAVE
    save(populations)