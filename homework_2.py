import datetime

from functools import wraps


# exercise number 1
def my_wraps(to_be_decorated):
    def wrap(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.__name__ = to_be_decorated.__name__
        wrapper.__doc__ = to_be_decorated.__doc__
        wrapper.__module__ = to_be_decorated.__module__
        wrapper.__qualname__ = to_be_decorated.__qualname__
        wrapper.__annotations__ = to_be_decorated.__annotations__
        return wrapper

    return wrap


# exercise number 2
def is_correct(*args):
    def wrap(func):
        def wrapped():
            counter = 0
            for arg in args:
                if arg in func():
                    counter += 1
            if counter == len(args):
                return func()
            else:
                return None

        return wrapped

    return wrap


# exercise number 3
def add_date(date_format):
    def wrap(func):
        @wraps(func)
        def wrapped():
            data = func()
            data['date'] = datetime.datetime.now().strftime(date_format)
            return data

        return wrapped

    return wrap
