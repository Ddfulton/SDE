# -*- encoding: utf-8 -*-
"""
    flask_triangle.modifiers.base
    -----------------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import unicode_literals
from __future__ import absolute_import


class Modifier(object):
    """
    """

    def alter_attrs(self, widget):
        pass

    def alter_schema(self, widget):
        pass

    def apply_to(self, widget):
        self.alter_attrs(widget)
        self.alter_schema(widget)
