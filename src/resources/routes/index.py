# -*- coding: utf-8 -*-

import traceback
from database import db
from database import redis_client
from models.md_short_url import MdShortUrl
from flask import redirect, url_for, make_response, abort, Blueprint

bp_index = Blueprint("index", __name__)


@bp_index.route("/<short_url>", methods=["GET"])
def index_url(short_url : str) -> make_response:
    try:
        redirect_url = redis_client.get(short_url)
        if redirect_url:
            return make_response(redirect(redirect_url, code=302), 302)

        with db.session() as session:
            url = MdShortUrl.query.filter_by(short_url=short_url).first()
            if not url:
                return abort(404)

            return make_response(redirect(url.redirect_url, code=302), 302)

    except Exception:
        traceback.print_exc()
        return abort(503)
