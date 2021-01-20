import os
import random
import json
from varname import nameof

random.seed(74)
OUT_PATH = '../out/'


LAMBDA = 100 # number of elements in new population
MI = 100 # number of elements in initial population
CROSSOVER_PROB = 1
KNEE = 2 # number of crossover points
MUTATION_PROB = 0.05

config_str = "lambda{}-mi{}-pc{}-knee{}/".format(LAMBDA, MI, CROSSOVER_PROB, KNEE)
save_directory = os.path.join(OUT_PATH, config_str)
if not os.path.exists(save_directory):
    os.makedirs(save_directory)
def save(var):
    with open(os.path.join(save_directory, nameof(var)), 'w') as f:
        json.dump(var, f)
