from sndlibparser import demand_array
from fitness import *
import random

link_keys = [
        (0, 1),
        (0, 2),
        (1, 3),
        (1, 5)
    ]

Link_0_1_data = {
        'demand': 101.00,
        'admissiblePaths': [
            [(0, 1), (1, 2)]
        ]
    }

Link_0_2_data = {
        'demand': 110.00,
        'admissiblePaths': [
            [(0, 1), (1, 2)],
            [(0, 3), (3, 10)],
            [(0, 5), (5, 7), (7, 8)]
        ]
    }

links = {
    0: {
        1: Link_0_1_data,
        2: Link_0_2_data
    },
    1: {
        3: Link_0_1_data,
        5: Link_0_2_data
    }
}

nodes_loads = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def createInitPopulationDistributed(mi):
    population = []
    for _ in range(mi):
        chromosome = []

        for link_start, link_rest in links.items():
            for link_end, link_data in link_rest.items():
                paths_no = len(link_data['admissiblePaths'])
                for index in range(paths_no):
                    chromosome.append(random.uniform(0, 1))

        fitness = calc_fitness_distributed(chromosome)
        population.append((chromosome, fitness))
    return population


def createInitPopulationAggregated(mi):
    population = []
    for _ in range(mi):
        chromosome = [random.randrange(len(paths)) for paths in demand_array]
        fitness = calc_fitness_aggregated(chromosome)
        population.append((chromosome, fitness))
    return population


def createInitPopulation(mi, is_distributed):
    if is_distributed:
        return createInitPopulationAggregated(mi)
    else:
        return createInitPopulationDistributed(mi)