#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask


def create_app() -> Flask:
    from models import db
    from flask_cors import CORS

    app = Flask(__name__)
    app.config.from_object("config")

    db.init_app(app)
    CORS(app)

    from okved.routes import bp as bp_okved

    app.register_blueprint(bp_okved, url_prefix="/okved")

    return app
