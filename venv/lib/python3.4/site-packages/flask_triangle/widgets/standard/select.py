# -*- encoding: utf-8 -*-
"""
    flask_triangle.widgets.select
    -----------------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

from flask_triangle.widget import Widget
import flask_triangle.modifiers


class Select(Widget):
    """HTML select element with angular data-binding"""

    schema = {'type': 'string'}

    html_template = ('<select {widget.attributes}>'
                     '{{widget.render_options()}}'
                     '</select>')

    def __customize__(self, options, required=False, multiple=False):

        if required is not False:
            self.modifiers.append(flask_triangle.modifiers.Required(required))
        if multiple:
            self.modifiers.append(flask_triangle.modifiers.Multiple())

        if isinstance(choices, list):
            self.choices = choices
        else:
            self.html_attributes['data-ng-options'] = choices

    def render_options(self):
        res = ''
        if self.choices is not None:
            choices = sorted([option + (None, None)[0:3-len(option)]
                              for option in self.choices], key=lambda x: x[2])

            current_group = None
            for title, value, group in choices:
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
