from sndlibparser import demand_array
import random

def addChromosome():
    return [random.randrange(len(paths)) for paths in demand_array]

def createInitPopulation(mi):
    return [addChromosome() for _ in range(mi)]