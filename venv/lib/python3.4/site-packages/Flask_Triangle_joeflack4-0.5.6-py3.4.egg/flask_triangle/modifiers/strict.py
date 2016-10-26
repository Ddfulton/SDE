# -*- encoding: utf-8 -*-
"""
    flask_triangle.modifiers.strict
    -------------------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import unicode_literals
from __future__ import absolute_import

from flask_triangle.modifiers.base import Modifier


class Strict(Modifier):

    def __init__(self, strict=True):

        self.strict = strict

    def alter_schema(self, widget):

        if self.strict:
            for k, v in widget.schema:
                if k != widget.bind:
                    v.additional_properties = not(self.strict)
