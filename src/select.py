from settings import settings, get_logger
import sys
import random

logger = get_logger('select')

# (default binary) tournament selection without replacement
def select(population, k):
    logger.debug(f"competition population: {population}")
    ret_list = []
    TOURNAMENT_COMPETITION_COUNT = settings["TOURNAMENT_COMPETITION_COUNT"]
    logger.debug(f"competition size: {TOURNAMENT_COMPETITION_COUNT}")

    for _ in range(k):
        # COMPETITION (SZRANKI)
        competition_chromosomes = random.sample(population, TOURNAMENT_COMPETITION_COUNT)
        logger.debug(f"competition chromosomes {competition_chromosomes}")
        best_chromosome = None
        best_fitness = sys.maxsize
        for chromosome, fitness in competition_chromosomes:
            if fitness < best_fitness:
                best_chromosome = chromosome
                best_fitness = fitness
        
        logger.debug(f"best chromosome {best_chromosome} and fitness {best_fitness}")
        if not best_chromosome:
            logger.error('Chromosome in tournament selection not found')
            sys.exit(1)
        ret_list.append(best_chromosome)

    if len(ret_list) != k:
        logger.error('Size of selection list is not compatible with ret elements desired count')
        sys.exit(1)
    return ret_list[0] if k == 1 else ret_list


# population = [('a', 1), ('b', 2), ('c', 3), ('d', 4), ('e', 4), ('f', 5), ('g', 6)]
# logger.debug(str(select(population, k=3)))