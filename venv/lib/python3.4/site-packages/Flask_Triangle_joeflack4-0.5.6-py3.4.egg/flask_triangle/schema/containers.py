# -*- encoding: utf-8 -*-
"""
    flask_triangle.schema.containers
    --------------------------------

    Include all the primitive types as defined in the JSON schema draft and
    which are of container type.

    http://tools.ietf.org/html/draft-zyp-json-schema-04

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

import copy, jsonschema

from .base import BaseType


class Object(BaseType):

    def __init__(self, min_properties=0, max_properties=False, required=False,
                 additional_properties=True, **kwargs):

        super(Object, self).__init__('object', **kwargs)

        self.min_properties = min_properties
        self.max_properties = max_properties
        self.additional_properties = additional_properties
        self.required = required or []

        self.properties = dict()

    def __iter__(self):

        yield (None, self)
        for k, v in self.properties.items():
            if hasattr(v, 'properties'):
                for sk, sv in v:
                    if sk is None:
                        yield (k, sv)
                    else:
                        yield ('{}.{}'.format(k, sk), sv)
            else:
                yield (k, v)

    def __contains__(self, name):

        if '.' not in name:
            return name in self.properties
        local, child = name.split('.', 1)
        if local in self.properties:
            return child in self.properties[local]
        else:
            return False

    def __getitem__(self, name):

        if '.' not in name:
            return self.properties[name]
        local, child = name.split('.', 1)
        return self.properties[local][child]

    def __setitem__(self, name, value):


        if '.' not in name:
            self.properties[name] = value
        else:
            local, child = name.split('.', 1)
            if self.properties.get(local, None) is None:
                self.properties[local] = Object()
            self.properties[local][child] = value


    def schema(self):

        res = super(Object, self).schema()

        if self.required: res['required'] = list(set(self.required))
        if self.min_properties: res['minProperties'] = self.min_properties
        if self.max_properties: res['maxProperties'] = self.max_properties

        if self.additional_properties is not True:
            res['additionalProperties'] = self.additional_properties

        res['properties'] = dict([
            (k, v.schema()) for k, v in self.properties.items()
        ])

        return res


class Schema(Object):

    def __init__(self, title=False, description=False, **kwargs):

        super(Schema, self).__init__(**kwargs)

        self.title = title
        self.description = description

    def schema(self):

        res = super(Schema, self).schema()

        if self.title: res['title'] = self.title
        if self.description: res['description'] = self.description

        return res


class Array(BaseType):

    def __init__(self, items, min_items=0, max_items=False, unique_items=False,
                 **kwargs):

        super(Array, self).__init__('array', **kwargs)

        self.items = items
        self.min_items = min_items
        self.max_items = max_items
        self.unique_items = unique_items

    def schema(self):

        res = super(Array, self).schema()

        res['items'] = [item.schema() for item in self.items]
        if self.min_items: res['minItems'] = self.min_items
        if self.max_items: res['maxItems'] = self.max_items
        if self.unique_items: res['uniqueItems'] = self.unique_items

        return res
