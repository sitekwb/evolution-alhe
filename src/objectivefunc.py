from settings import settings, get_logger

logger = get_logger('objectivefunc')


# returns true if stop
def stop_condition(generation, stale_generations, fitness):
    if settings["MAX_GENERATIONS"] < generation:
        logger.debug("Max generations count achieved. Stopping.")
        return True
    if settings["MAX_STALE_GENERATIONS"] < stale_generations:
        logger.debug("Max stale generations count achieved. Stopping.")
        return True
    if settings["TARGET_FITNESS"] > fitness:    # minimizing fitness
        logger.debug("Target fitness achieved. Stopping.")
        return True
    else:
        return False
