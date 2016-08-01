# -*- encoding: utf-8 -*-
"""
    flask_triangle.widget
    ---------------------

    Implement the Widget base class.

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

import sys, jinja2, copy, inspect

from flask_triangle.schema import Schema
from flask_triangle.helpers import HTMLString, HTMLAttrs


class Widget(object):
    """
    """

    # the instance counter is used to keep track of the widget order in a form.
    instance_counter = 0

    # the default HTML template
    html_template = (
        '<em>'
        'This widget is not renderable.'
        '</em>'
    )

    # the atomic_schema
    atomic_schema = None

    @property
    def bind(self):
        return self.html_attributes.get('ngModel', None)

    @bind.setter
    def bind(self, value):
        self.html_attributes['ngModel'] = value

    @property
    def name(self):
        return self.html_attributes.get('name', None)

    @name.setter
    def name(self, value):
        self.html_attributes['name'] = value

    @property
    def label(self):
        if self._label is None:
            return self.name
        return self._label

    @label.setter
    def label(self, value):
        self._label = value

    def __init__(self, bind, name=None, label=None, description=None,
                 html_attributes=None, modifiers=None, **kwargs):

        # increment the instance counter
        self.instance_counter = Widget.instance_counter
        Widget.instance_counter += 1

        self.html_attributes = HTMLAttrs()
        self.schema = Schema()
        self.modifiers = []

        # default properties
        self.bind = bind                # is an HTML attribute (see properties)
        self.name = name                # is an HTML attribute (see properties)
        self.label = label
        self.description = description

        if self.atomic_schema is not None:
            self.schema[bind] = copy.deepcopy(self.atomic_schema)

        self._apply_customize(**kwargs)

        # final user's stuff override everything else
        if modifiers is not None:
            self.modifiers += modifiers
        if html_attributes is not None:
            self.html_attributes.update(html_attributes)

        self.apply_modifiers()

    def _apply_customize(self, **kwargs):
        """
        A recusive method calling each customize method found in the inheritance
        tree of the widget.
        """

        def recursion(cls):

            if cls.__base__ != Widget:
                recursion(cls.__base__)

            customize = getattr(cls, 'customize', None)
            if customize is not None:
                # Get the list minus the first argument (self)
                args = inspect.getargspec(customize).args[1:]
                customize(
                    self,
                    **dict((k, v) for k, v in kwargs.items() if k in args)
                )

        if self.__class__ is not Widget:
            recursion(self.__class__)

    def apply_modifiers(self):

        for modifier in self.modifiers:
            modifier.apply_to(self)

    def __unicode__(self):

        return jinja2.Template(self.html_template).render(
            widget=self,
            attrs=self.html_attributes
        )

    def __str__(self):
        # Python2/3 compatibility
        if sys.version_info > (3, 0):
            return self.__unicode__()
        return unicode(self).encode('utf-8')
