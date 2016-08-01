# -*- encoding: utf-8 -*-
"""
    flask_triangle.modifiers.limits
    -------------------------------

    A collection of modifiers for Flask-Triangle's widgets.

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from .limits import Limit, LengthLimit
from .required import Required
from .patterns import Regexp
from .strict import Strict

__all__ = ['Required', 'Limit', 'LengthLimit', 'Regexp', 'Strict']
