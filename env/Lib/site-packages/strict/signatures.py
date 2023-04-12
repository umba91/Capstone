# -*- coding: utf-8 -*-
"""
Constraint objects
==================

"""


import abc
import itertools
import collections
import six


__all__ = ("Signature",)


class Signature(object):

    """

    """

    def __init__(self, owner, *args, **kwargs):
        self.owner = owner
        self.args_constraints = args
        self.kwargs_constraints = kwargs

    def _validate(self, callback, *args, **kwargs):
        # First, check the args
        for constraints, value in itertools.izip(self.args_constraints, args):
            if not isinstance(constraints, collections.Iterable):
                # assume, that it's a single value
                callback(self.owner, constraints, value)
            else:
                for constraint in constraints:
                    callback(self.owner, constraint, value)

        # Then the kwargs
        for key, value in six.iteritems(kwargs):
            if key in self.kwargs_constraints:
                constraints = self.kwargs_constraints[key]
                if not isinstance(constraints, collections.Iterable):
                    callback(self.owner, constraint, value)
                else:
                    for constraint in constraints:
                        callback(self.owner, constraint, value)
            else:
                raise TypeError(
                    "{owner} got unexpected keyword argument "
                    "'{kwarg}'.".format(
                        owner=self.owner,
                        kwarg=key))

    def is_valid(self, *args, **kwargs):
        result = []

        def callback(owner, constraint, value):
            result.append(constraint(value))

        self._validate(callback, *args, **kwargs)
        return all(result)

    def claim(self, *args, **kwargs):
        def callback(owner, constraint, value):
            constraint.claim(owner, value)
        self._validate(callback, *args, **kwargs)
