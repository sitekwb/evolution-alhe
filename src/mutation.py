from sndlibparser import demand_array
from settings import settings, get_logger
import random

logger = get_logger('mutation')

def mutation(chromosome):
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
            possibilities = len(demand_array[index]) # for debug
            logger.debug(f'Size of this gene possibilities: {possibilities}, array of possibilities: {demand_array[index]}')
            chromosome[index] = random.randrange(len(demand_array[index]))
        chosen_gene = chromosome[index] # for debug
        logger.debug(f"Randomly mutated gene: {chosen_gene}")
    return chromosome
