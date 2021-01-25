from sndlibparser import demand_array
from settings import settings, get_logger
import random

logger = get_logger('mutation')

def mutation(chromosome):
    MUTATION_PROB = settings["MUTATION_PROB"]
    p = random.uniform(0, 1)
    # mutate only with MUTATION_PROB
    if p < MUTATION_PROB:
        # choose one gene for mutation         
        index = random.randrange(len(chromosome))
        # mutate chosen gene
        if settings["DISTRIBUTED"]:
            chromosome[index] = random.uniform(0, 1)
        else:
            chromosome[index] = random.randrange(len(demand_array[index]))
    return chromosome
