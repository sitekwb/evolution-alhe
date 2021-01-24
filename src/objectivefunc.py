from settings import settings


def stop_condition(generation, stale_generations, fitness):
    if settings["MAX_GENERATIONS"] < generation:
        return True
    if settings["MAX_STALE_GENERATIONS"] < stale_generations:
        return True
    if settings["TARGET_FITNESS"] > fitness:    # minimizing fitness
        return True
    else:
        return False
    # returns true if stop
