# -*- encoding: utf-8 -*-
"""
    flask_triangle.widgets.standard.text
    ------------------------------------

    Implement the base widgets of HTML5 supported by AngularJS.

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

from flask_triangle.widgets import Widget
from flask_triangle.schema import String, Number
from flask_triangle.modifiers import Required


class Input(Widget):
    """
    The default input widget.
    """
    atomic_schema = String()
    html_template = (
        '<input{%if attrs%} {{attrs}}{%endif%}>'
        '</input>'
    )

    def customize(self, required=False, min_length=0, max_length=False,
                  pattern=False, change=False):

        if required:
            self.modifiers.append(Required(required))
        if min_length:
            self.modifiers.append(MinimumLength(min_length))
        if max_length:
            self.modifiers.append(MaximumLength(max_length))
        if pattern:
            self.modifiers.append(Regexp(pattern))
        if change:
            self.html_attributes['ngChange'] = change



class TextInput(Input):
    """
    """

    def customize(self, trim=True):

        self.html_attributes['type'] = 'text'
        if trim is not True:
            self.html_attributes['ngTrim'] = trim


class PasswordInput(Input):
    """
    """

    def options(self):

        self.html_attributes['type'] = 'password'



'''
class Textarea(Input):
    """
    HTML textarea element control with angular data-binding.
    """
    html_template = '<textarea {{attr}}></textarea>'



class EmailInput(Input):
    """
    """
    pass

    schema = Email()

    def __init__(self, bind, name=None, label=None, modifiers=None,
                 metadata=None, **kwargs):

        kwargs['type'] = 'email'
        super(EmailInput, self).__init__(bind, name, label, modifiers, metadata,
                                         **kwargs)

class NumberInput(Input):
    """
    """

    schema = Number()

    def __init__(self, bind, name=None, label=None, modifiers=None,
                 metadata=None, **kwargs):

        kwargs['type'] = 'number'
        super(NumberInput, self).__init__(bind, name, label, modifiers, metadata,
                                          **kwargs)
'''
