import threading
import time
import json


class MutableVariable:
    def __init__(self, value):
        self.value = value


def memoize(expiration_time=60):
    def decorator(func):
        cache = {}
        lock = threading.Lock()
        th = MutableVariable(None)

        def cleanup():
            current_time = time.time()
            with lock:
                keys_to_delete = [
                    key for key, (timestamp, _) in cache.items() if current_time - timestamp > expiration_time
                ]
                for key in keys_to_delete:
                    del cache[key]

        def update_cache(args, kwargs):
            key = json.dumps(args)
            cache[key] = (time.time(), func(*args, **kwargs))

        def wrapper(*args, **kwargs):
            key = json.dumps(args)
            cleanup()
            if key not in cache:
                result = func(*args, **kwargs)
                cache[key] = (time.time(), result)
            else:
                if th.value != None:
                    th.value.join()
                    th.value = None
                _, result = cache[key]
                th.value = threading.Thread(target=lambda: update_cache(args, kwargs))
                th.value.start()
            return result

        return wrapper

    return decorator
