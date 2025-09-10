import os
import cProfile

from config import PROFILING_DIR

def get_profile_path(func_name):
    return os.path.join(PROFILING_DIR, f"{func_name}.prof")

def profiling(func):
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        func_name = func.__name__
        profiler.dump_stats(get_profile_path(func_name))
        return result
    return wrapper

def safe_profiling(func):
    def wrapper(*args, **kwargs):
        try:
            return profiling(func)(*args, **kwargs)
        except RuntimeError:  
            return func(*args, **kwargs)
    return wrapper
