import logging
from settings import MODULARITY, DISTRIBUTED

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

nodes_loads = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def ceildiv(a, b):
    return -(-a // b)


# na to jeszcze nie patrzyłem po zmianach w parserze
def calc_fitness_aggregated(chromosome):
    gene_i = 0
    for link_start, link_rest in links.items():
        for link_end, link_data in link_rest.items():
            path_index = chromosome[gene_i]
            path = link_data['admissiblePaths'][path_index]
            start_node_i = path[0][0]
            nodes_loads[start_node_i] += link_data['demand']
            for edge in path:
                nodes_loads[edge[1]] += link_data['demand']

            logging.debug(f"loads: {nodes_loads}")
            gene_i += 1

    if len(chromosome) != gene_i:
        logging.error("Individual does not represent valid genotype")

    fitness = 0
    for load in nodes_loads:
        fitness += ceildiv(load, MODULARITY)
        logging.debug(f"Load: {load}, mod: {MODULARITY}, fitness: {fitness}")

    logging.debug(f"Fitness: {fitness}")

    return fitness


def calc_fitness_distributed(chromosome):
    gene_i = 0
    for link_start, link_rest in links.items():
        for link_end, link_data in link_rest.items():
            paths_no = len(link_data['admissiblePaths'])
            paths = link_data['admissiblePaths']

            genes = chromosome[gene_i:gene_i + paths_no]
            genes_total = sum(genes)
            if genes_total == 0:
                logging.warning("All genes had value 0, forcing load on first path")
                genes[0] = 1
                genes_total = 1
            genes_normalized = [gene/genes_total for gene in genes]

            for index in range(paths_no):
                path = paths[index]
                start_node_i = path[0][0]
                nodes_loads[start_node_i] += link_data['demand'] * genes_normalized[index]
                for edge in path:
                    nodes_loads[edge[1]] += link_data['demand'] * genes_normalized[index]

            logging.debug(f"loads after link: {nodes_loads}")
            gene_i += paths_no

    if len(chromosome) != gene_i:
        logging.error("Invididual does not represent vaild genotype")

    nodes_loads[-1] = 0.00000000000006

    fitness = 0
    for load in nodes_loads:
        fitness += ceildiv(load - 0.00001, MODULARITY)        # TODO co z ogonkiem? przykład z wyżej pokazuje problemix
        logging.debug(f"Load: {load}, mod: {MODULARITY}, fitness: {fitness}")

    logging.debug(f"Fitness: {fitness}")

    return fitness


def calc_fitness(chromosome):
    if DISTRIBUTED == 1:
        return calc_fitness_distributed(chromosome)
    else:
        return calc_fitness_aggregated(chromosome)


#   calc_fitness_aggregated([0,2,0,1], 50)
calc_fitness_distributed([0.37, 0.20, 0.10, 0.3, 0, 1, 1, 1])
