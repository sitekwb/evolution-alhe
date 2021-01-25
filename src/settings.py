import os
import random
import json
import logging
from varname import nameof

#  random.seed(74)

def get_logger(filename):
    format_str = '%(asctime)s --- %(levelname)s --- %(name)s --- %(message)s'
    logging.basicConfig(format=format_str)
    formatter = logging.Formatter(format_str)
    logger = logging.getLogger('alhe.{}'.format(filename))
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('out.txt')
    fh.setFormatter(formatter)
    logger.propagate = True
    logger.addHandler(fh)
    return logger

OUT_PATH = '../out/'
logger = get_logger('settings')

settings = {
        "LAMBDA": 100,  # number of elements in new population
        "MI": 100,  # number of elements in initial population
        "CROSSOVER_PROB": 1,
        "CROSSOVER_POINTS_COUNT": 2,  # number of crossover points
        "MUTATION_PROB": 0.05,
        "TARGET_FITNESS": 15,
        "MAX_GENERATIONS": 20,
        "MAX_STALE_GENERATIONS": 3,
        "DISTRIBUTED": False,
        "MODULARITY": 50,
        "TOURNAMENT_COMPETITION_COUNT": 2,
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

    logger.info("Settings loaded:" + str(settings))


load_config("config.txt")   # TODO its here just for testing

config_str = "lambda{}-mi{}-pc{}-crossoverpointscount{}/".format(settings["LAMBDA"], settings["MI"], settings["CROSSOVER_PROB"], settings["CROSSOVER_POINTS_COUNT"])
save_directory = os.path.join(OUT_PATH, config_str)
if not os.path.exists(save_directory):
    os.makedirs(save_directory)


def save(var):
    with open(os.path.join(save_directory, nameof(var)), 'w') as f:
        json.dump(var, f)
