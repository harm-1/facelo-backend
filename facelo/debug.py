from functools import wraps

from flask import request
from facelo.user.serializers import UserSchema


def wrap_bp(func):

    @wraps(func)
    def newFunc(*args, **kwargs):
        breakpoint()
        return func(*args, **kwargs)

    return newFunc


# UserSchema().load(request.json)
