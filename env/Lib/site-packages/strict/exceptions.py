# -*- coding: utf-8 -*-
"""
Strict Function Exceptions
==========================

"""


import abc
import textwrap
import six


__all__ = (
    "SubjectConstraintError",
    "TypeConstraintError")


@six.add_metaclass(abc.ABCMeta)
class ConstraintError(Exception):
    """
    """

    def __init__(self, owner, expected, got):
        self.owner = owner
        self.expected = expected
        self.got = got
        super(ConstraintError, self).__init__(self.message)

    @abc.abstractproperty
    def message_template(self):
        raise NotImplementedError("Purely abstract property.")

    @abc.abstractproperty
    def message(self):
        raise NotImplementedError("Purely abstract property.")


class SubjectConstraintError(ConstraintError, ValueError):
    """
    This exception represents an error, when some value does not correspond to
    the expected, domain specific constraint.
    """

    def __init__(self, owner, predicate_fn, value):
        super(SubjectConstraintError, self).__init__(owner, predicate_fn, value)

    @property
    def message_template(self):
        result = textwrap.dedent("""
            {owner} caused a subject constraint violation: {value}.
            """)

        if hasattr(self.expected, "__doc__"):
            if self.expected.__doc__ and self.expected.__doc__.strip():
                result = " ".join([result, self.expected.__doc__])

        return result.replace("\n", "")

    @property
    def message(self):
        return self.message_template.format(
            owner=repr(self.owner),
            value=repr(self.got))


class TypeConstraintError(ConstraintError, TypeError):
    """
    An exception, that signifies a violated type constraint and produces a nice
    error message.
    """

    def __init__(self, owner, type_expected, got):
        super(TypeConstraintError, self).__init__(owner, type_expected, got)

    @property
    def message_template(self):
        result = textwrap.dedent("""
            {owner} caused a type constraint violation. Expected {type} and got 
            {value} of {value_type}.
            """)
        return result.replace("\n", "")

    @property
    def message(self):
        return self.message_template.format(
            owner=repr(self.owner),
            type=repr(self.expected),
            value=repr(self.got),
            value_type=repr(type(self.got)))
