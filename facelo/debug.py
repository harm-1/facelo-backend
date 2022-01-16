from functools import wraps

from flask import request


def wrap_bp(func):

    @wraps(func)
    def newFunc(*args, **kwargs):
        breakpoint()
        return func(*args, **kwargs)

    return newFunc
