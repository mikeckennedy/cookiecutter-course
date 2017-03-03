# -*- coding: utf-8 -*-
from bottle import Bottle, jinja2_view


home_app = Bottle()


@home_app.route('/')
@jinja2_view('index.html')
def index():
    return {'get_url': home_app.get_url}


