from sndlibparser import demand_array
from fitness import *
import random
from settings import DISTRIBUTED

def createInitPopulationDistributed(mi):
    population = []
    for _ in range(mi):
        chromosome = []

        for demand_data in demand_array:
            paths_no = len(demand_data['admissiblePaths'])
            for index in range(paths_no):
                chromosome.append(random.uniform(0, 1))

        fitness = calc_fitness_distributed(chromosome)
        population.append((chromosome, fitness))
    return population


def createInitPopulationAggregated(mi):
    population = []
    for _ in range(mi):
        chromosome = [random.randrange(len(demand_data['admissiblePaths'])) for demand_data in demand_array]
        fitness = calc_fitness_aggregated(chromosome)
        population.append((chromosome, fitness))
    return population


def createInitPopulation(mi):
    if DISTRIBUTED == 1:
        return createInitPopulationDistributed(mi)
    else:
        return createInitPopulationAggregated(mi)