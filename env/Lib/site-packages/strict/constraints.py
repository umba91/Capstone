# -*- coding: utf-8 -*-
"""
Constraint objects
==================

"""


import abc
import types
import six
import strict.exceptions as exs


__all__ = (
    "TypeConstraint",
    "SubjectConstraint")


class BaseConstraint(object):
    """
    """

    @abc.abstractmethod
    def claim(self, owner, some_value):
        pass

    @abc.abstractmethod
    def __call__(self, some_value):
        pass

    @abc.abstractproperty
    def exception_class(self):
        pass


class TypeConstraint(BaseConstraint):
    """
    Represent a type constraint, that can be either checked or asserted 
    against.
    """
    def __init__(self, expected_type):
        self.expected_type = expected_type

    def claim(self, owner, some_value):
        if not isinstance(some_value, self.expected_type):
            raise self.exception_class(
                owner,
                self.expected_type,
                some_value)

    def __call__(self, some_value):
        return isinstance(some_value, self.expected_type)

    @property
    def expected_type(self):
        return self._expected_type

    @expected_type.setter
    def expected_type(self, value):
        if not isinstance(value, six.class_types):
            raise exs.TypeConstraintError(
                owner=self,
                type_expected=type,
                got=type(value))
        else:
            self._expected_type = value

    @property
    def exception_class(self):
        return exs.TypeConstraintError


class SubjectConstraint(BaseConstraint):
    """
    Represents a subject matter constraint.
    """
    def __init__(self, predicate_fn):
        self.predicate_fn = predicate_fn

    def claim(self, owner, value):
        if not self.predicate_fn(value):
            raise self.exception_class(
                owner,
                self.predicate_fn,
                value)

    def __call__(self, value):
        return self.predicate_fn(value) 

    @property
    def predicate_fn(self):
        return self._predicate_fn

    @predicate_fn.setter
    def predicate_fn(self, value):
        if not six.callable(value):
            raise exs.TypeConstraintError(
                owner=self,
                type_expected=types.FunctionType,
                got=type(value))
        else:
            self._predicate_fn = value
    
    @property
    def exception_class(self):
        return exs.SubjectConstraintError
