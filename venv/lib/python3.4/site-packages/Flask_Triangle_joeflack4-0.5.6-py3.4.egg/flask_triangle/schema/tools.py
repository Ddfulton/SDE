# -*- encoding: utf-8 -*-
"""
    flask_triangle.schema.tools
    ---------------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

import copy
from flask_triangle.schema import Schema, Object

def schema_merger(*schemas):
    """
    Merge multiple schemas in a new-one.
    """

    res = Schema(description='Generated with Flask-Triangle')

    for schema in schemas:
        for k, v in schema:
            if k is not None and k not in res and isinstance(v, Object):
                res[k] = Object()
            elif not isinstance(v, Object):
                res[k] = copy.deepcopy(v)

            if hasattr(v, 'required') and k is not None:
                res[k].required += [prop for prop in v.required
                                          if prop not in res[k].required]
            elif hasattr(v, 'required'):
                res.required += [prop for prop in v.required
                                       if prop not in res.required]

    return res
