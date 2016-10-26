# -*- encoding: utf-8 -*-
"""
    flask_triangle.modifiers.patterns
    ---------------------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import unicode_literals
from __future__ import absolute_import

from flask_triangle.modifiers.base import Modifier


class Regexp(Modifier):

    def __init__(self, regexp, client=True):
        """
        """
        self.client = client
        self.regexp = regexp

    def alter_attrs(self, widget):

        if self.client is True:
            widget.html_attributes['ngPattern'] = self.regexp

    def alter_schema(self, widget):
        target = widget.schema[widget.bind]
        target.pattern = self.regexp
