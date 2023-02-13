# -*- coding: utf-8 -*-

import traceback
from database import db
from datetime import datetime
from database import redis_client
from models.md_short_url import MdShortUrl
from flask import redirect, url_for, make_response, abort, Blueprint, jsonify

bp_index = Blueprint("index", __name__)


@bp_index.route("/<short_url>", methods=["GET"])
def index_short_url(short_url : str) -> make_response:
    try:
        redirect_url = redis_client.get(short_url)
        if redirect_url:
            print("Redirect with cache ->", redirect_url)
            return make_response(redirect(redirect_url, code=302), 302)

        with db.session() as session:
            now = datetime.now()
            url = MdShortUrl.query.filter_by(short_url=short_url).first()
            if not url:
                return abort(404)

            if url.valid_at < now:
                return make_response(
                    jsonify({
                        "response": "Your ShortUrl is experired!",
                        "status": 403
                    }), 403)

            delta = url.valid_at - now
            redis_client.set(short_url, url.redirect_url, ex=int(round(delta.total_seconds(), 0)))
            print("Redirect with db ->", url.redirect_url)
            return make_response(redirect(url.redirect_url, code=302), 302)

    except Exception:
        traceback.print_exc()
        return abort(503)
