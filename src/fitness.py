import logging
import random

from sndlibparser import demand_array, link_keys
from settings import settings

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


def ceildiv(a, b):
    return -(-a // b)


def calc_fitness_aggregated(chromosome):
    MODULARITY = settings["MODULARITY"]
    gene_i = 0
    edges_loads = [0] * len(link_keys)
    for demand_data in demand_array:
        path_index = chromosome[gene_i]
        path = demand_data['admissiblePaths'][path_index]
        for edge in path:
            link_index = link_keys.index(edge)
            edges_loads[link_index] += demand_data['demand']

        logging.debug(f"loads: {edges_loads}")
        gene_i += 1

    if len(chromosome) != gene_i:
        logging.error("Individual does not represent valid genotype")

    fitness = 0
    for load in edges_loads:
        fitness += ceildiv(load, MODULARITY)
        logging.debug(f"Load: {load}, mod: {MODULARITY}, fitness: {fitness}")

    logging.debug(f"Fitness: {fitness}")

    return fitness


def calc_fitness_distributed(chromosome):
    MODULARITY = settings["MODULARITY"]
    gene_i = 0
    edges_loads = [0] * len(link_keys)

    for demand in demand_array:
        paths_no = len(demand['admissiblePaths'])
        paths = demand['admissiblePaths']

        genes = chromosome[gene_i:gene_i + paths_no]
        genes_total = sum(genes)
        if genes_total == 0:
            logging.warning("All genes for this demand had value 0, forcing load on first path")
            genes[0] = 1
            genes_total = 1

        genes_normalized = [gene / genes_total for gene in genes]

        for index in range(paths_no):
            path = paths[index]
            for edge in path:
                link_index = link_keys.index(edge)
                edges_loads[link_index] += demand['demand'] * genes_normalized[index]

            logging.debug(f"loads after link: {edges_loads}")
        gene_i += paths_no

    if len(chromosome) != gene_i:
        logging.error("Individual does not represent valid genotype")

    fitness = 0
    for load in edges_loads:
        fitness += ceildiv(load - 0.00001, MODULARITY)        # safeguard against incorrect roundings
        logging.debug(f"Load: {load}, mod: {MODULARITY}, fitness: {fitness}")

    logging.debug(f"Fitness: {fitness}")

    return fitness


def calc_fitness(chromosome):
    if settings["DISTRIBUTED"]:
        return calc_fitness_distributed(chromosome)
    else:
        return calc_fitness_aggregated(chromosome)


demand_array = demand_array[0:4]
for demand in demand_array:
    demand['admissiblePaths'] = demand['admissiblePaths'][0:2]

chromosome = []
for demand in demand_array:
    for path in demand['admissiblePaths']:
        chromosome.append(random.random())

chromosome[0:7] = [0.1, 0.2, 0.3, 0.1, 0.1, 0.1, 0.1]

chromosome_agg = [0, 1, 0, 1]

print(chromosome)
calc_fitness_aggregated(chromosome_agg)
calc_fitness_distributed(chromosome)
