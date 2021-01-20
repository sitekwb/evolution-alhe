import logging

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

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


def ceildiv(a, b):
    return -(-a // b)


def calc_fitness_aggregated(individual, modularity):
    gene_i = 0
    for link_start, link_rest in links.items():
        for link_end, link_data in link_rest.items():
            path_index = individual[gene_i]
            path = link_data['admissiblePaths'][path_index]
            start_node_i = path[0][0]
            nodes_loads[start_node_i] += link_data['demand']
            for edge in path:
                nodes_loads[edge[1]] += link_data['demand']

            logging.debug(f"loads: {nodes_loads}")
            gene_i +=1

    if len(individual) != gene_i:
        logging.error("Invididual does not represent vaild genotype")

    fitness = 0
    for load in nodes_loads:
        fitness += ceildiv(load, modularity)
        logging.debug(f"Load: {load}, mod: {modularity}, fitness: {fitness}")

    logging.debug(f"Fitness: {fitness}")

    return fitness

def calc_fitness_distributed(individual, modularity):
    gene_i = 0
    for link_start, link_rest in links.items():
        for link_end, link_data in link_rest.items():
            paths_no = len(link_data['admissiblePaths'])
            paths = link_data['admissiblePaths']

            genes = individual[gene_i:gene_i + paths_no]
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

    if len(individual) != gene_i:
        logging.error("Invididual does not represent vaild genotype")

    nodes_loads[-1] = 0.00000000000006

    fitness = 0
    for load in nodes_loads:
        fitness += ceildiv(load - 0.00001, modularity)        # TODO co z ogonkiem? przykład z wyżej pokazuje problemix
        logging.debug(f"Load: {load}, mod: {modularity}, fitness: {fitness}")

    logging.debug(f"Fitness: {fitness}")

    return fitness


#calc_fitness_aggregated([0,2,0,1], 50)
calc_fitness_distributed([0.37, 0.20, 0.10, 0.3, 0, 1, 1, 1], 50)