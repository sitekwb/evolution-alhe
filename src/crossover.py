import random
import logging
from settings import settings, get_logger

logger = get_logger('crossover')


def crossover(elements):     # list of 2 elements, number of crossover points
    crossover_points_count = settings["CROSSOVER_POINTS_COUNT"]
    logger.debug(f"Parent0:    {elements[0]}")
    logger.debug(f"Parent1:    {elements[1]}")
    crossover_points = set()
    while len(crossover_points) != crossover_points_count:
        crossover_points.add(random.randrange(len(elements[0])))
    crossover_points.sort()
    logger.debug(f"Chosen crossover points: {crossover_points}, len(elements[0]): {len(elements[0])}")
    crossover_points.append(len(elements[0]))

    offspring = []
    start = 0
    parent_no = 0
    for point in crossover_points:
        offspring += elements[parent_no][start:point]
        parent_no = (parent_no + 1) % 2
        start = point

    logger.debug(f"Offspring:  {offspring}")

    return offspring

#  crossover([[10,11,12,13,14,15,16,17,18,19], [20,21,22,23,24,25,26,27,28,29]], 3)
