from sndlibparser import demand_array
from settings import settings, get_logger
import random

logger = get_logger('mutation')


def mutation(chromosome):
    ch = chromosome
    if settings["MUTATION_FREQUENCY"] == -1:
        return single_mutation(ch)

    for _ in range(settings["MUTATION_FREQUENCY"]):
        ch = single_mutation(ch)
    return ch


def single_mutation(chromosome):
    MUTATION_PROB = settings["MUTATION_PROB"]
    p = random.uniform(0, 1)
    # mutate only with MUTATION_PROB
    if p < MUTATION_PROB:
        logger.debug(f'Mutating! Mutation prob is {MUTATION_PROB}')
        # choose one gene for mutation         
        index = random.randrange(len(chromosome))
        logger.debug(f"Random index: {index}")
        chosen_gene = chromosome[index] # for debug
        logger.debug(f"Chosen gene: {chosen_gene}")
        # mutate chosen gene
        if settings["DISTRIBUTED"]:
            chromosome[index] = random.uniform(0, 1)
        else:
            possibilities_array = demand_array[index]['admissiblePaths']
            possibilities_count = len(possibilities_array)
            logger.debug(f'Size of this gene possibilities: {possibilities_count}')
            chromosome[index] = random.randrange(possibilities_count)
        chosen_gene = chromosome[index] # for debug
        logger.debug(f"Randomly mutated gene: {chosen_gene}")
    return chromosome
