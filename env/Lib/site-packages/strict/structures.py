# -*- coding: utf-8 -*-
"""
Structures
==========

"""


__all__ = (
    "Structure",
    "Field",

    "ListSerialization",
    "ListDeserialization",

    "DictSerialization",
    "DictDeserialization",

    # "JSONSerialization",   # TODO
    # "JSONDeserialization"  # TODO
)


import abc
import six

from strict.functions import *
from strict.constraints import TypeConstraint, SubjectConstraint


class Field(object):
    # Check constraints not only on __set__, but also on __get__.
    be_paranoid = False

    # Name template for protected attributes in the owner objects.
    protected_name = "_{attr_name}"

    # Internal creation counter, that captures the declaration order of a
    # Field. This works both in Python 2 and 3...
    _declaration_counter = 0

    def __init__(self, type_, *check_fns):
        self.type_constraint = TypeConstraint(type_)
        self.subject_constraints = [SubjectConstraint(fn) for fn in check_fns]

        type(self)._declaration_counter += 1
        self.declaration_order = self._declaration_counter

        # To be filled by the metaclass
        self.name = None

    def __get__(self, owner, cls):
        if not owner:
            return self
        else:
            attr = self.protected_name.format(attr_name=self.name)
            result = getattr(owner, attr)
            if self.be_paranoid:
                self.claim_constraints(result)
            return result

    def __set__(self, owner, value):
        self.claim_constraints(value)
        attr = self.protected_name.format(attr_name=self.name)
        setattr(owner, attr, value)

    def __repr__(self):
        return "<{module}.{cls_name}: attr={attr}>".format(
            module=getattr(self, "__module__"),
            cls_name=type(self).__name__,
            attr=self.name)

    def claim_constraints(self, value):
        self.type_constraint.claim(self, value)
        for subject_constraint in self.subject_constraints:
            subject_constraint.claim(self, value)


class StructureMeta(type):

    def __new__(self, cls_name, bases, attrs):
        slots = []
        fields = []
        for name, attr in six.iteritems(attrs):
            if isinstance(attr, Field):
                pname = Field.protected_name.format(attr_name=name)
                order = attr.declaration_order  # FIXME

                attr.name = name
                slots.append(pname)
                fields.append((name, order))  # FIXME

        # Slots
        if slots:
            if "__slots__" in attrs:
                attrs["__slots__"].extend(slots)
            else:
                attrs["__slots__"] = slots

        attrs["fields"] = [name
                           for name, _
                           in sorted(fields, key=lambda f: f[1])]

        return type.__new__(self, cls_name, bases, attrs)


@six.add_metaclass(StructureMeta)
class Structure(object):

    def to_dict(self, cls=dict):
        serialization = DictSerialization(result_cls=cls)
        return serialization(self)

    @classmethod
    def from_dict(cls, dict_obj):
        deserialization = DictDeserialization()
        return deserialization(dict_obj, cls)

    def to_list(self, with_tuples=False):
        serialization = ListSerialization(with_tuples)
        return serialization(self)

    @classmethod
    def from_list(cls, list_obj, with_tuples=False):
        deserialization = ListDeserialization(with_tuples)
        return deserialization(list_obj)

    @classmethod
    def default_constructor(cls, **kwargs):
        """
        This is a default constructor, that should have the same interface for 
        all Structure classes and descendant classes.
        """
        new_struct = cls.__new__(cls)

        for key, value in six.iteritems(kwargs):
            setattr(new_struct, key, value)

        return new_struct


@six.add_metaclass(abc.ABCMeta)
class BaseSerialization(object):

    # It makes sense here to decorate the methods, since the whole
    # functionality of the class relies on being supplied a Structure class
    # and not on some well known protocol, like that of a dict.
    @expects(self, arg(Structure))
    def __call__(self, struct):
        result_set = self.new_result_set()
        for name in struct.fields:
            attribute = getattr(struct, name)
            if isinstance(attribute, Structure):
                self.add_field(
                    result_set,
                    name,
                    self(attribute))
            else:
                self.add_field(
                    result_set,
                    name,
                    attribute)
        return result_set

    @abc.abstractmethod
    def new_result_set(self):
        pass

    @abc.abstractmethod
    def add_field(self, result_set, name, field):
        pass


@six.add_metaclass(abc.ABCMeta)
class BaseDeserialization(object):

    # And since this is a base class and we can't be sure, how the abstract
    # parts will be implemented later, it makes sense to control the output of
    # the __call__ method, as a logical counterpart to __init__'s constraints.
    @returns(Structure)
    def __call__(self, obj, result_cls):
        init_dict = {}

        for field_name in result_cls.fields:
            field_descriptor = getattr(result_cls, field_name)
            field_type_constraint = field_descriptor.type_constraint

            container_key = self.key(result_cls, field_name)
            value = self.fetch_from_container(obj, container_key)

            if issubclass(field_type_constraint.expected_type, Structure):
                init_dict[field_name] = self(
                    value,
                    field_type_constraint.expected_type)
            else:
                init_dict[field_name] = value

        return result_cls.default_constructor(**init_dict)

    @abc.abstractmethod
    def key(self, struct, key_alias):
        """
        This function should translate "key_alias" to something the container 
        object may understand. So for example, if the container object is a 
        list, then we might need the translation field_name -> order
        """
        pass

    @abc.abstractmethod
    def fetch_from_container(self, container_obj, container_key):
        pass


class DictDeserialization(BaseDeserialization):

    def key(self, struct, key_alias):
        return key_alias

    def fetch_from_container(self, container_obj, container_key):
        return container_obj[container_key]


class ListDeserialization(BaseDeserialization):

    def __init__(self, with_tuples=False):
        self.with_tuples = with_tuples

    def key(self, struct, key_alias):
        return struct.fields.index(key_alias)

    def fetch_from_container(self, container_obj, container_key):
        item = container_obj[container_key]
        if self.with_tuples:
            _, value = item
        else:
            value = item
        return value


class DictSerialization(BaseSerialization):

    def __init__(self, result_cls=dict):
        """
        `result_cls` may be any dict-like class.
        """
        self.result_cls = result_cls

    def new_result_set(self):
        return self.result_cls()

    def add_field(self, result_set, name, field):
        result_set[name] = field
        return result_set


class ListSerialization(BaseSerialization):

    def __init__(self, with_tuples=False):
        self.with_tuples = with_tuples

    def new_result_set(self):
        return list()

    def add_field(self, result_set, name, field):
        if self.with_tuples:
            item = name, field
        else:
            item = field

        result_set.append(item)
        return result_set