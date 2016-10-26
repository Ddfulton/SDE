# -*- encoding: utf-8 -*-
"""
    flask_triangle.widgets.special.label
    ------------------------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

from flask_triangle.widget import Widget


class Label(Widget):
    """
    Simple text rendering in a <span> element.
    """

    html_template = ('<span {{widget.html_attributes}}>'
                     '{{ \'{{{{\' + widget.bind + \'|angular}}}}\' }}'
                     '</span>')

    @property
    def bind(self):
        return self._bind

    @bind.setter
    def bind(self, value):
        self._bind = value
