from sndlibparser import nodes, links
from mutation import mutation
from crossover import crossover
from select import select
from objectivefunc import stop_condition
from init import createInitPopulation
from fitness import *
from settings import MI, CROSSOVER_PROB, CROSSOVER_POINTS_COUNT, LAMBDA, save

import sys
import random


# WOJTEK:
# MAIN
# PARSER
# MUTATION
# INIT

# KACPER:
# KOSZTA Z WĘZŁÓW NA KRAWĘDZIE
# RESZTA


def find_best_individual(population):
    best_fitness = sys.maxsize
    best_chromosome = None
    for chromosome, fitness in population:
        if fitness < best_fitness:
            best_fitness = fitness
            best_chromosome = chromosome
    return (best_chromosome, best_fitness)


if __name__ == 'main':
    populations = []
    # initialize population and set time to 0
    populations.append(createInitPopulation(MI)) # MI elements
    t = 0
    # initialize count of generations not getting better to 0
    stale_generations_count = 0
    lowest_fitness = sys.maxsize
    while not stop_condition(t, stale_generations_count, lowest_fitness):
        temporary_population = []
        for i in range(LAMBDA):
            a = random.uniform(0, 1)
            if a < CROSSOVER_PROB:
                chromosome = mutation(crossover(select(populations[t], k=2), CROSSOVER_POINTS_COUNT))
                fitness = calc_fitness(chromosome)
                temporary_population.append((chromosome, fitness))
            else:
                chromosome = mutation(select(populations[t], 1))
                fitness = calc_fitness(chromosome, DISTRIBUTED)
                temporary_population.append((chromosome, fitness))

        best_chromosome, best_fitness = find_best_individual(temporary_population)
        if best_fitness > lowest_fitness:
            stale_generations_count += 1
        else:
            stale_generations_count = 0
            lowest_fitness = best_fitness

        populations.append(temporary_population)
        t += 1
    
    # SAVE
    save(populations)