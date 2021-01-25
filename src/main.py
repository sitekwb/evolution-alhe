from settings import settings, save
from mutation import mutation
from crossover import crossover
from select import select
from objectivefunc import stop_condition
from init import createInitPopulation
from fitness import *

import sys
import random

logger = get_logger('main')
print(__name__)

if __name__ == '__main__':
    MI = settings["MI"]
    populations = []
    winner_chromosome = None
    # initialize population and set time to 0
    logger.debug(f"Creating init population with {MI} chromosomes")
    populations.append(createInitPopulation(MI))  # MI elements
    t = 0
    # initialize count of generations not getting better to 0
    stale_generations_count = 0
    lowest_fitness = sys.maxsize
    while not stop_condition(t, stale_generations_count, lowest_fitness):
        temporary_population = []
        for i in range(settings["LAMBDA"]):
            a = random.uniform(0, 1)
            if a < settings["CROSSOVER_PROB"]:
                logger.debug("Entering crossover section")
                logger.debug("Getting new chromosome")
                chromosome = mutation(crossover(select(populations[t], k=2)))
                logger.debug("Calculating fitness")
                fitness = calc_fitness(chromosome)
                logger.debug("Appending chromosome with fitness to population")
                temporary_population.append((chromosome, fitness))
            else:
                logger.debug("No crossover in this generation")
                logger.debug("Getting new chromosome")
                chromosome = mutation(select(populations[t], k=1))
                logger.debug("Calculating fitness")
                fitness = calc_fitness(chromosome)
                logger.debug("Appending chromosome with fitness to population")
                temporary_population.append((chromosome, fitness))

        logger.debug("Finding best individual")
        best_chromosome, best_fitness = find_best_individual(temporary_population)
        logger.info(f'Best fitness in this generation is {best_fitness}')
        if best_fitness > lowest_fitness:
            stale_generations_count += 1
            logger.debug(f'It is a stale generation repeated {stale_generations_count} time')
        else:
            logger.debug(f"Best generation ever. Chromosome {best_chromosome} with fitness {best_fitness}")
            stale_generations_count = 0
            lowest_fitness = best_fitness
            winner_chromosome = best_chromosome

        populations.append(temporary_population)
        t += 1
        logger.debug("Going to the next generation")
    
    # SAVE
    save(populations)
