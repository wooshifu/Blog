from functools import wraps
from flask import Flask

from app import app as blog_app

__before_request_func_priority = []


def before_request(priority: int, app: Flask = blog_app):
    """
    register before_request based on priority

    :param app: Flask app
    :param priority: priority
    """

    def wrapper(func):
        @wraps(func)
        def wrap():
            __before_request_func_priority.append((func, priority))
            __before_request_func_priority.sort(key=lambda func_priority: func_priority[1], reverse=True)
            app.before_request_funcs[None] = [f[0] for f in __before_request_func_priority]

        return wrap()

    return wrapper
