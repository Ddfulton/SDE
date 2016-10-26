# -*- encoding: utf-8 -*-
"""
    flask_triangle.validators.type
    ------------------------------

    Validators to modify and verify the return type of a widget.

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import unicode_literals
from __future__ import absolute_import

from flask_triangle.modifiers.base import Modifier
from flask_triangle.schema.natural import String, Integer, Number, Boolean


class AsSpecified(Modifier):

    def alter_schema(self, widget):
        widget.schema[widget.bind] = alternate_type


class AsString(AsSpecified):

    alternate_type = String()


class AsInteger(AsSpecified):

    alternate_type = Integer()


class AsNumber(AsSpecified):

    alternate_type = Number()


class AsBoolean(AsSpecified):

    alternate_type = Boolean()
