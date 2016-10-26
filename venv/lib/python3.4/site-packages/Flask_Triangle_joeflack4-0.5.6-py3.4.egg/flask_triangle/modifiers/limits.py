# -*- encoding: utf-8 -*-
"""
    flask_triangle.modifiers.limits
    -------------------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import unicode_literals
from __future__ import absolute_import

from flask_triangle.modifiers.base import Modifier


class Limit(Modifier):

    def __init__(self, minimum=0, maximum=False):

        self.minimum = minimum
        self.maximum = maximum

    def alter_attrs(self, widget):

        if self.minimum:
            widget.html_attributes['min'] = self.minimum
        if self.maximum:
            widget.html_attributes['max'] = self.maximum

    def alter_schema(self, widget):
        target = widget.schema[widget.bind]
        if self.minimum:
            target.minimum = self.minimum
        if self.maximum:
            target.maximum = self.maximum



class LengthLimit(Modifier):

    def __init__(self, minimum=0, maximum=False):

        self.minimum = minimum
        self.maximum = maximum

    def alter_attrs(self, widget):

        if self.minimum:
            widget.html_attributes['ngMinlength'] = self.minimum
        if self.maximum:
            widget.html_attributes['ngMaxlength'] = self.maximum

    def alter_schema(self, widget):

        target = widget.schema[widget.bind]

        if self.minimum:
            target.min_length = self.minimum
        if self.maximum:
            target.max_length = self.maximum
