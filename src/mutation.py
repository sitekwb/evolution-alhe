from sndlibparser import demand_array
from settings import MUTATION_PROB, DISTRIBUTED
import random

def mutation(chromosome):
    p = random.uniform(0, 1)
    # mutate only with MUTATION_PROB
    if p < MUTATION_PROB:
        # choose one gene for mutation         
        index = random.randrange(len(chromosome))
        # mutate chosen gene
        if DISTRIBUTED == 1:
            chromosome[index] = random.uniform(0, 1)
        else:
            chromosome[index] = random.randrange(len(demand_array[index]))
    return chromosome


def mutationDistributed(chromosome):
