# -*- coding: utf-8 -*-

from flask import Flask
from database import db, redis_client
from flask_restful import Api
from flask_migrate import Migrate
from resources.api.short_url import ShortUrlApi
from resources.routes.index import bp_index

# APP FLASK
app =  Flask(__name__)

# CONFIG
app.config.from_pyfile("config.py")
db.init_app(app)
redis_client.init_app(app)
migrate = Migrate(app, db)

# API's
api = Api(app)
api.add_resource(ShortUrlApi, "/api/short-url")

# Blueprint's
app.register_blueprint(bp_index)
