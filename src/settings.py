import os
import random
import json
import logging
from varname import nameof

#random.seed(74)
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
OUT_PATH = '../out/'

settings = {
        "LAMBDA": 100,  # number of elements in new population
        "MI": 100,  # number of elements in initial population
        "CROSSOVER_PROB": 1,
        "KNEE": 2,  # number of crossover points
        "MUTATION_PROB": 0.05,
        "TARGET_FITNESS": 15,
        "MAX_GENERATIONS": 20,
        "MAX_STALE_GENERATIONS": 3,
        "DISTRIBUTED": False,
        "MODULARITY": 50
    }


def load_config(path):
    try:
        config = open(path, "rt")
        lines = config.readlines()
        for line in lines:
            setting = line.rstrip().split('=')
            settings[setting[0]] = int(setting[1])
        if settings["DISTRIBUTED"] == 1:
            settings["DISTRIBUTED"] = True
        elif settings["DISTRIBUTED"] == 0:
            settings["DISTRIBUTED"] = False
        config.close()
    except FileNotFoundError:
        print(f'File "{path}" not found. Make sure it is in the same folder as python files.\nDefault values will be loaded.')

    logging.info("Settings loaded:" + str(settings))

load_config("config.txt")   # TODO its here just for testing

config_str = "lambda{}-mi{}-pc{}-knee{}/".format(settings["LAMBDA"], settings["MI"], settings["CROSSOVER_PROB"], settings["KNEE"])
config_str = "lambda{}-mi{}-pc{}-knee{}/".format(LAMBDA, MI, CROSSOVER_PROB, CROSSOVER_POINTS_COUNT)
save_directory = os.path.join(OUT_PATH, config_str)
if not os.path.exists(save_directory):
    os.makedirs(save_directory)


def save(var):
    with open(os.path.join(save_directory, nameof(var)), 'w') as f:
        json.dump(var, f)
