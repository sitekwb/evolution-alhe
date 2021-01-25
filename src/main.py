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
    populations = []
    winner_chromosome = None
    # initialize population and set time to 0
    populations.append(createInitPopulation(settings["MI"]))  # MI elements
    t = 0
    # initialize count of generations not getting better to 0
    stale_generations_count = 0
    lowest_fitness = sys.maxsize
    while not stop_condition(t, stale_generations_count, lowest_fitness):
        temporary_population = []
        for i in range(settings["LAMBDA"]):
            a = random.uniform(0, 1)
            if a < settings["CROSSOVER_PROB"]:
                chromosome = mutation(crossover(select(populations[t], k=2)))
                fitness = calc_fitness(chromosome)
                temporary_population.append((chromosome, fitness))
            else:
                chromosome = mutation(select(populations[t], k=1))
                fitness = calc_fitness(chromosome)
                temporary_population.append((chromosome, fitness))

        best_chromosome, best_fitness = find_best_individual(temporary_population)
        if best_fitness >= lowest_fitness:
            stale_generations_count += 1
        else:
            stale_generations_count = 0
            lowest_fitness = best_fitness
            winner_chromosome = best_chromosome

        logger.info(f"Generation {t}: stale: {stale_generations_count}, lowest fitness: {lowest_fitness}")

        populations.append(temporary_population)
        t += 1

    logger.info(f"Winner individual: {lowest_fitness}, {winner_chromosome}")

    # SAVE
    save(populations)
