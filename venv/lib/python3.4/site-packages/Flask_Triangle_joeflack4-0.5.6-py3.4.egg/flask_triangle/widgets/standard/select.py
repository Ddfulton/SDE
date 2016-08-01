# -*- encoding: utf-8 -*-
"""
    flask_triangle.widgets.select
    -----------------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

from flask_triangle.widgets.widget import Widget
import flask_triangle.modifiers


class Select(Widget):
    """HTML select element with angular data-binding"""

    schema = {'type': 'string'}

    html_template = ('<select {{attr}}>'
                     '{{widget.render_options()}}'
                     '</select>')

    def __init__(self, bind, options, name=None, label=None, modifiers=None,
                 metadata=None, **kwargs):

        if isinstance(options, list):
            self._options = options
        else:
            self._options = None
            kwargs['data-ng-options'] = options
        super(Select, self).__init__(bind, name, label, modifiers, metadata,
                                     **kwargs)

    def render_options(self):

        res = ''

        if self._options is not None:
            # create three-element tuples
            options = sorted(
                [list(option) + [None, None][0:3-len(option)] for option in self._options],
                key=lambda x: x[2] or ''
            )

            current_group = None
            for title, value, group in options:
                if group != current_group:
                    if current_group is not None:
                        res += '</optgroup>'
                    res += '<optgroup label="{}">'.format(group)
                    current_group = group

                if value is not None:
                    res += '<option value="{}">{}</option>'.format(value, title)
                else:
                    res += '<option>{}</option>'.format(title)
            if current_group is not None:
                res += '</optgroup>'
        return res
