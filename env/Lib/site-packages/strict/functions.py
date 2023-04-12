# -*- coding: utf-8 -*-
"""

"""

import functools
from strict.signatures import Signature
from strict.constraints import *


__all__ = (
    "any_arg",
    "self",
    "arg",
    "expects",
    "returns")


def any_arg():
    return []


self = any_arg()


def arg(type_, check_fn=lambda x: True):
    return (TypeConstraint(type_), SubjectConstraint(check_fn))


def expects(*arg_constraints, **kwarg_constraints):
    def decorator(fn):
        arg_signature = Signature(
            fn,
            *arg_constraints,
            **kwarg_constraints)

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            arg_signature.claim(*args, **kwargs)
            return fn(*args, **kwargs)

        wrapper.expects = arg_signature
        return wrapper
    return decorator


def returns(type_, check_fn=lambda x: True):
    def decorator(fn):
        ret_signature = Signature(
            fn, arg(type_, check_fn))

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            result = fn(*args, **kwargs)
            ret_signature.claim(result)
            return result

        wrapper.returns = ret_signature
        return wrapper
    return decorator
