import time
from cachetools import TTLCache

cache = TTLCache(maxsize=100, ttl=8.57)
request_timestamps = []

def is_rate_limited():
    current_time = time.time()
    global request_timestamps
    request_timestamps = [t for t in request_timestamps if current_time - t < 60]
    return len(request_timestamps) >= 7