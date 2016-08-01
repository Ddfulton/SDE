# -*- encoding: utf-8 -*-
"""
    flask_triangle.schema.base
    --------------------------

    The base type of all types used in a JSON Schema.

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

import sys, json
from six import text_type


class BaseType(object):

    def __init__(self, type_, enum=False, all_of=False, any_of=False,
                 one_of=False, is_not=False):

        self.type_ = type_
        self.is_not = is_not
        self.enum = enum or []
        self.all_of = all_of or []
        self.any_of = any_of or []
        self.one_of = one_of or []

    def __hash__(self):
        return hashlib.sha1(repr(self))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __repr__(self):
        return text_type(self)

    def __unicode__(self):
        return json.dumps(self.schema(), sort_keys=True)

    def __str__(self):
        # Python2/3 compatibility
        if sys.version_info > (3, 0):
            return self.__unicode__()
        return unicode(self).encode('utf-8')

    def schema(self):

        res = {'type': self.type_}
        if self.enum: res['enum'] = self.enum
        if self.all_of: res['allOf'] = [i.schema for i in self.all_of]
        if self.any_of: res['anyOf'] = [i.schema for i in self.any_of]
        if self.one_of: res['oneOf'] = [i.schema for i in self.one_of]
        if self.is_not: res['not'] = self.is_not.schema

        return res
