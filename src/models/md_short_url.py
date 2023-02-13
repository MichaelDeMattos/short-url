# -*- coding: utf-8 -*-

from database import db
from datetime import datetime

class MdShortUrl(db.Model):
    __tablename__ = "short_url"

    id = db.Column(db.Integer, primary_key=True)
    redirect_url = db.Column(db.String(1024), nullable=False)
    short_url = db.Column(db.String(64), unique=True, nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    valid_at = db.Column(db.DateTime, nullable=True)
