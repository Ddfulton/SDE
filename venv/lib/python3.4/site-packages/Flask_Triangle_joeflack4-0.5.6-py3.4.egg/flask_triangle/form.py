# -*- encoding: utf-8 -*-
"""
    flask_triangle.form
    -------------------

    Implements the Form class.

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import

import copy, jsonschema
from six import add_metaclass
from flask_triangle.widgets import Widget
from flask_triangle.schema import schema_merger


class FormBase(type):
    """Metaclass for a Form object"""

    def __new__(mcs, name, bases, attrs):

        super_new = super(FormBase, mcs).__new__
        parents = [b for b in bases if isinstance(b, mcs)]

        if not parents:
            return super_new(mcs, name, bases, attrs)

        new_class = super_new(
            mcs, name, bases,
            {'__module__': attrs.pop('__module__')}
        )

        new_class._form_widget_list = copy.deepcopy(new_class._form_widget_list)
        new_widgets = list()

        for obj_name, obj in attrs.items():
            setattr(new_class, obj_name, obj)
            if isinstance(obj, Widget):

                if obj.name is None:
                    obj.name = obj_name

                if obj_name not in new_class._form_widget_list:
                    new_widgets.append(obj_name)

            elif obj_name in new_class._form_widget_list:
                new_class._form_widget_list.remove(obj_name)

        new_widgets.sort(key=lambda k: getattr(new_class, k).instance_counter)
        new_class._form_widget_list += new_widgets

        return new_class


@add_metaclass(FormBase)
class Form(object):
    """
    """

    _form_widget_list = list()

    @property
    def schema(self):
        if self._vroot is not None:
            return self._schema[self._vroot]
        return self._schema

    def __init__(self, vroot=None, strict=True, alternate_schema=None):
        """
        """

        self._vroot = vroot
        if alternate_schema is not None:
            self._schema = copy.deepcopy(alternate_schema)
        else:
            wschemas = [getattr(self, k).schema for k in self._form_widget_list]
            self._schema = schema_merger(*wschemas)

        # apply strict to the schema
        if strict:
            for k, v in self._schema:
                if hasattr(v, 'additional_properties'):
                    v.additional_properties = not strict

    def __iter__(self):
        return (getattr(self, obj_name) for obj_name in self._form_widget_list)


def validate(form, json):

    return jsonschema.validate(json, form.schema)
