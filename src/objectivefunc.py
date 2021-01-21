from settings import TARGET_FITNESS, MAX_GENERATIONS, MAX_STALE_GENERATIONS


def stop_condition(generation, stale_generations, fitness):
    if (MAX_GENERATIONS < generation):
        return True
    if (MAX_STALE_GENERATIONS < stale_generations):
        return True
    if (TARGET_FITNESS > fitness): # minimizing fitness
        return True
    else:
        return False
    # returns true if stop