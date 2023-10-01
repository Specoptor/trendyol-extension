import time


def timer(func):
    """Decorator for timing functions.
    :param func: function to be timed
    :return: wrapper
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed = end_time - start_time.__round__(3)
        print(f'{func.__name__} took {elapsed} seconds')
        return result

    return wrapper
