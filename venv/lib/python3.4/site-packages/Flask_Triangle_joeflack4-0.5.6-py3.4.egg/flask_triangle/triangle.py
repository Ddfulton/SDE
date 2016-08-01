#-*- encoding: utf-8 -*-
"""
    flask_triangle.triangle
    -----------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

from flask import request, abort
from flask_triangle.jinja import angular_filter, TriangleUndefined


class Triangle(object):
    """
    Central controller class that can be used to configure how Flask-Triangle
    behaves. Each application that wants to use Flask-Triangle has to create,
    or run :meth:`init_app` on, an instance of this class after the
    configuration was initialized.
    """

    def __init__(self, app=None):

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Set up this instance for use with *app*, if no app was passed to the
        constructor.
        """

        # set the Jinja2 environment
        app.jinja_env.undefined = TriangleUndefined
        app.jinja_env.filters['angular'] = angular_filter
