from sndlibparser import nodes, links
from mutation import mutation
from crossover import crossover
from select import select
from objectivefunc import stop_condition
from init import createInitPopulation
from fitness import *
from settings import MI, CROSSOVER_PROB, KNEE, LAMBDA, save, DISTRIBUTED

import sys
import random


def find_best_individual(population):
    fitness = sys.maxsize
    for individual in population:
        if fitness > individual[1]:
            fitness = individual[1]
            best = individual
    return individual


if __name__ == 'main':
    populations = []
    populations.append(createInitPopulation(MI, DISTRIBUTED)) # MI elements
    t = 0
    stale_generations = 0
    lowest_fitness = sys.maxsize
    while not stop_condition(t, stale_generations, lowest_fitness):
        temporary_population = []
        for i in range(LAMBDA):
            a = random.uniform(0, 1)
            if a < CROSSOVER_PROB:
                chromosome = mutation(crossover(select(populations[t], 2), KNEE))
                fitness = calc_fitness(chromosome, DISTRIBUTED)
                temporary_population.append((chromosome, fitness))
            else:
                mutation(select(populations[t], 1))
                fitness = calc_fitness(chromosome, DISTRIBUTED)
                temporary_population.append((chromosome, fitness))

        best_indiv = find_best_individual(temporary_population)
        if best_indiv[1] > lowest_fitness:
            stale_generations += 1
        else:
            stale_generations = 0
            lowest_fitness = best_indiv[1]

        populations.append(temporary_population)
        t += 1
    
    # SAVE
    save(populations)