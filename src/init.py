from sndlibparser import demand_array
from fitness import *
import random

def addChromosomeAggregated():
    return [random.randrange(len(paths)) for paths in demand_array]

def createInitPopulationAggregated(mi):
    population = []
    for _ in range(mi):
        chromosome = addChromosomeAggregated()
        fitness = calc_fitness_aggregated(chromosome)
        population.append((chromosome, fitness))
    return population