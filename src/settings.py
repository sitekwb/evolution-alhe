from ast import increment_lineno
import os
import random
import json
import logging

OUT_DIR = '../out/'
CONFIG_DIR = '../config/'

settings = {
        "LAMBDA": 100,  # number of elements in new population
        "MI": 100,  # number of elements in initial population
        "CROSSOVER_PROB": 1,
        "CROSSOVER_POINTS_COUNT": 2,  # number of crossover points
        "MUTATION_PROB": 0.05,
        "TARGET_FITNESS": 100,
        "MAX_GENERATIONS": 20,
        "MAX_STALE_GENERATIONS": 10,
        "DISTRIBUTED": False,
        "MODULARITY": 50,
        "TOURNAMENT_COMPETITION_COUNT": 2,
        "SEED": 74,
        "SHOW_LOG_ON_CONSOLE": False,
        "MUTATION_FREQUENCY": 0.1,
    }

def load_config(path):
    try:
        with open(path, "rt") as config:
            lines = config.readlines()
            for line in lines:
                try:
                    setting = line.rstrip().split('=')
                    settings[setting[0]] = int(setting[1])
                except ValueError:
                    setting = line.rstrip().split('=')
                    if setting[0] in {"CROSSOVER_PROB", "MUTATION_PROB", "MUTATION_FREQUENCY"}:
                        settings[setting[0]] = float(setting[1])
                    else:
                        logger.warning(f"Only probabilities can be float (failed to parse {setting})")
        if settings["DISTRIBUTED"] == 1:
            settings["DISTRIBUTED"] = True
        elif settings["DISTRIBUTED"] == 0:
            settings["DISTRIBUTED"] = False
        settings["SHOW_LOG_ON_CONSOLE"] = True if settings["SHOW_LOG_ON_CONSOLE"] == 1 else False
    except FileNotFoundError:
        print(f'File "{path}" not found. Make sure it is in the same folder as python files.\nDefault values will be loaded.')

load_config(os.path.join(CONFIG_DIR, "config.txt"))

# NOT USED TODO REMOVE
# config_str = "lambda{}-mi{}-cp{}-cpc{}-mp{}-distr{}-mod{}-szr{}".format(
#     settings["LAMBDA"],
#     settings["MI"],
#     settings["CROSSOVER_PROB"],
#     settings["CROSSOVER_POINTS_COUNT"],
#     settings["MUTATION_PROB"],
#     1 if settings["DISTRIBUTED"] else 0,
#     settings['MODULARITY'],
#     settings['TOURNAMENT_COMPETITION_COUNT']
# )

RUNID_FILENAME = os.path.join(CONFIG_DIR, f"runid.txt")
RUNID_WAS_IN_SETTINGS = False

def serve_runid():
    if "RUNID" in settings:
        RUNID_WAS_IN_SETTINGS = True
        return
    if os.path.isfile(RUNID_FILENAME):
        with open(RUNID_FILENAME) as f:
            runid = int(f.read())
    else:
        runid = 1

    settings["RUNID"] = str(runid)

serve_runid()

save_directory = os.path.join(OUT_DIR, settings["RUNID"])
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

def save(var, name):
    with open(os.path.join(save_directory, f"{name}.json"), 'w') as f:
        json.dump(var, f)

random.seed(settings["SEED"])

def get_logger(filename):
    format_str = '%(asctime)s --- %(levelname)s --- %(name)s --- %(message)s'
    logging.basicConfig(format=format_str)
    formatter = logging.Formatter(format_str)
    logger = logging.getLogger('alhe.{}'.format(filename))
    logger.setLevel(logging.INFO)
    # TODO remove print(filename, os.path.join(OUT_DIR, settings["RUNID"], "log.out"))
    fh = logging.FileHandler(os.path.join(OUT_DIR, settings["RUNID"], "log.out"))
    fh.setFormatter(formatter)
    logger.propagate = settings['SHOW_LOG_ON_CONSOLE']
    logger.addHandler(fh)
    return logger

logger = get_logger('settings')
for key, value in settings.items():
    logger.info(f"Setting {key}: {value}")

def increment_runid():
    if not RUNID_WAS_IN_SETTINGS:
        with open(RUNID_FILENAME, 'w') as f:
            f.write(str(int(settings["RUNID"]) + 1))