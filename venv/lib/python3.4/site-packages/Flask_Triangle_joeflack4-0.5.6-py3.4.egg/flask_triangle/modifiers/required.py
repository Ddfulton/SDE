# -*- encoding: utf-8 -*-
"""
    flask_triangle.modifiers.required
    ---------------------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import unicode_literals
from __future__ import absolute_import

from flask_triangle.modifiers.base import Modifier


class Required(Modifier):

    def __init__(self, condition=True):

        self.condition = condition

    def alter_attrs(self, widget):

        if self.condition is True:
            widget.html_attributes['required'] = None
        elif self.condition:
            widget.html_attributes['ngRequired'] = self.condition

    def alter_schema(self, widget):

        if self.condition is True:
            properties = widget.bind.split('.')
            for i, (k, v) in enumerate(widget.schema):
                if i < len(properties):
                    v.required.append(properties[i])
