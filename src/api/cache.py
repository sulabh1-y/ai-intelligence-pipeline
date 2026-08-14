import time

CACHE = {
    "data": None,
    "timestamp": 0
}

CACHE_EXPIRY = 60  # seconds (1 minute)


def get_cache():
    current_time = time.time()

    # check if cache is valid
    if CACHE["data"] and (current_time - CACHE["timestamp"] < CACHE_EXPIRY):
        return CACHE["data"]

    return None


def set_cache(data):
    CACHE["data"] = data
    CACHE["timestamp"] = time.time()