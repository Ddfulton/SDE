# -*- encoding: utf-8 -*-
"""
    flask_triangle.schema
    ---------------------

    A set of tools to manage a JSON Schema.

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

from flask_triangle.schema.containers import Schema, Object, Array
from flask_triangle.schema.natural import Boolean, Integer, Number, String
from flask_triangle.schema.tools import schema_merger

__all__ = [
    'Schema', 'Object', 'Boolean', 'Integer', 'Number', 'String', 'Array',
]
