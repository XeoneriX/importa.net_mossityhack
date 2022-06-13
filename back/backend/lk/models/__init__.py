# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class OkvedCategory(db.Model):
    name = db.Column(db.String(8), primary_key=True)
    description = db.Column(db.String)
    
