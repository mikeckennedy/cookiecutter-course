# -*- coding: utf-8 -*-
from bottle import Bottle

from .controllers.home import home_app


Routes = Bottle()
# App to render / (home)
Routes.merge(home_app)
