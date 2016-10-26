# -*- encoding: utf-8 -*-
"""
    flask_triangle.helpers.html
    ---------------------------

    A set of tools to manipulate HTML.

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

import sys, re
from six import text_type



class HTMLString(text_type):
    """
    """

    def __html__(self):
        return self


class HTMLAttrs(object):
    """
    """

    @staticmethod
    def attr_name(string):
        """
        Compute a valid attribute name.
        """

        if re.match(r'^[A-Za-z0-9]+$', string):
            words = re.split(r'(^[a-z]*)|([A-Z][^A-Z]+)', string)
            return '-'.join(c for c in words if c is not None and c).lower()
        return string.lower()

    @staticmethod
    def attr_value(value):
        """
        Render the value as expected in the HTML :
        - double quotes
        - local handling of the angular filter
        """

        resp = '"{}"'

        # convert the value to a string
        if isinstance(value, bool):
            string = text_type(value).lower()
        else:
            string = text_type(value)

        if string.endswith('|angular'):
            string = '{{{{{}}}}}'.format(string[:-8])

        return resp.format(string)

    @staticmethod
    def render_attr(name, value):
        """
        Render one attribute as expected in the HTML.
        - key="value"
        """

        if value is None:
            return name
        return '{name}={value}'.format(name=name,
                                       value=HTMLAttrs.attr_value(value))

    def __init__(self, **kwargs):

        self.attributes = dict()

        for k, v in kwargs.items():
            self[k] = v

    def items(self):
        return self.attributes.items()

    def get(self, key, default):
        return self.attributes.get(self.attr_name(key), default)

    def __contains__(self, key):
        return self.attr_name(key) in self.attributes

    def __getitem__(self, key):
        return self.attributes[self.attr_name(key)]

    def __setitem__(self, key, value):
        self.attributes[self.attr_name(key)] = value

    def __delitem__(self, key):
        del self.attributes[self.attr_name(key)]

    def __iter__(self):
        return self.attributes.__iter__()

    def __unicode__(self):
        return ' '.join(self.render_attr(k, v) for k, v in sorted(self.items()))

    def __str__(self):
        # Python2/3 compatibility
        if sys.version_info > (3, 0):
            return self.__unicode__()
        return unicode(self).encode('utf-8')

    def update(self, kvp_iterable):
        for k, v in kvp_iterable.items():
            self[k] = v
