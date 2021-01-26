from settings import settings, save, increment_runid
from mutation import mutation
from crossover import crossover
from select import select
from objectivefunc import stop_condition
from init import createInitPopulation
from fitness import *
from tqdm import tqdm

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sys
import random

def plot(populations):
    fig, ax = plt.subplots()

    # Data for plotting
    for index in range(len(populations)):
        population = populations[index]
        x = [index] * len(population)
        _, y = zip(*population)
        plt.scatter(x, y, c = 'blue', s = 1)

    ax.set(xlabel='Generation', ylabel='Fitness',
           title='')    # TODO some data possibly
    ax.grid()

    fig.savefig("test.png")  # TODO namefile?
    plt.show()

if __name__ == '__main__':
    logger = get_logger('main')
    populations = []
    winner_chromosome = None
    lowest_fitness = sys.maxsize
    try:
        MI = settings["MI"]
        # initialize population and set time to 0
        logger.debug(f"Creating init population with {MI} chromosomes")
        populations.append(createInitPopulation(MI))  # MI elements
        t = 0
        # initialize count of generations not getting better to 0
        stale_generations_count = 0
        progress_bar = tqdm()
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
            logger.info(f'Generation: {t}; fitness: {best_fitness}')
            if best_fitness >= lowest_fitness:
                stale_generations_count += 1
                logger.debug(f'It is a stale generation repeated {stale_generations_count} time')
            else:
                logger.debug(f"Best generation ever. Chromosome {best_chromosome} with fitness {best_fitness}")
                logger.info(f"Generation: {t}; fitness: {best_fitness}. Best.")
                stale_generations_count = 0
                lowest_fitness = best_fitness
                winner_chromosome = best_chromosome

            populations.append(temporary_population)
            t += 1
            logger.debug("Going to the next generation")
            progress_bar.update()
            progress_bar.set_description(f"{lowest_fitness:9.2f}")
    except Exception as e:
        print(e)
    finally:
        plot(populations)
        # SAVE
        # save(populations, 'populations')
        save(winner_chromosome, 'winner_chromosome')
        save(lowest_fitness, 'lowest_fitness')
        save(settings, 'settings')
        increment_runid()
