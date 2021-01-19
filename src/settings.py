
random.seed(74)
OUT_PATH = '../out/'


LAMBDA = 100 # number of elements in new population
MI = 100 # number of elements in initial population
CROSSOVER_PROB = 0.3
K = 2 # number of elements selected for crossover 

config_str = "lambda{}-mi{}-pc{}-k{}/".format(LAMBDA, MI, CROSSOVER_PROB, K)
save_directory = os.path.join(OUT_PATH, config_str)
if not os.path.exists(save_directory):
    os.makedirs(save_directory)
def save(var):
    with open(os.path.join(save_directory, nameof(var)), 'w') as f:
        json.dump(var, f)
