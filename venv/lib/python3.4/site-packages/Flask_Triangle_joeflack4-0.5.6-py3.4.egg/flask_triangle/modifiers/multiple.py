# -*- encoding: utf-8 -*-
"""
    flask_triangle.modifiers.multiple
    ---------------------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import unicode_literals
from __future__ import absolute_import

from flask_triangle.modifiers.base import Modifier


class Multiple(Modifier):

    def __init__(self, min_items=0, max_items=0, unique_items=False):

        self.min_items = min_items
        self.max_items = max_items
        self.unique_items = unique_items

    def alter_html_attr(self, widget):

        widget.html_attrs['multiple'] = None

    def alter_schema(self, widget):

        target = widget.schema[widget.bind]
        widget.schema[widget.bind] = Array(target,
                                           min_items=self.min_items,
                                           max_items=self.max_items,
                                           unique_items=self.unique_items)
