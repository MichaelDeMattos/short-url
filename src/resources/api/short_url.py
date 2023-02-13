# -*- coding: utf-8 -*-

import os
import json
import traceback
from shortuuid import ShortUUID
from flask_restful import Resource
from database import db, redis_client
from datetime import datetime, timedelta
from models.md_short_url import MdShortUrl
from flask import make_response, jsonify, request, current_app, abort


class ShortUrlApi(Resource):
    def __init__(self, *args):
        ...

    def get(self):
        try:
            short_url = request.args.get("short_url")
            with db.session() as session:
                url = MdShortUrl.query.filter_by(short_url=short_url).first()

                if not url:
                    return abort(404)

                return make_response(
                    jsonify({
                        "response": {
                            "id": url.id,
                            "redirect_url": url.redirect_url,
                            "short_url": url.short_url,
                            "create_at": url.create_at,
                            "valid_at": url.valid_at
                        },
                        "status": 200
                    }), 200)

        except Exception as error:
            traceback.print_exc()
            return make_response(
                jsonify({
                    "response": str(error),
                    "status": 503}), 503)

    def post(self):
        try:
            body = request.data
            body = json.loads(body)
            redirect_url = body.get("redirect_url")
            size = body.get("size")
            valid_at = datetime.now() + timedelta(days=5)
            delta = valid_at - datetime.now()

            if size not in range(5, 11):
                return make_response(
                    jsonify({
                        "response": "Url size is incorret!",
                        "status": 403}), 403)
            try:
                with db.session() as session:
                    short_url = ShortUUID().random(length=size).lower()
                    new_short_url = MdShortUrl(
                        redirect_url=redirect_url,
                        short_url=short_url,
                        valid_at=valid_at)
                    session.add(new_short_url)
                    session.commit()
                    redis_client.set(short_url, redirect_url, ex=int(round(delta.total_seconds(), 0)))
                    return make_response(
                        jsonify({
                            "response": {
                                "message": "Short Url created with successfully!",
                                "data": os.path.join(current_app.config["APP_DOMAIN"], short_url)
                            },
                            "status": 201
                        }), 201)

            except Exception as error:
                traceback.print_exc()
                session.rollback()
                return make_response(
                    jsonify({
                        "response": str(error),
                        "status": 503
                    }), 503)

        except Exception as error:
            traceback.print_exc()
            return make_response(
                jsonify({
                    "response": str(error),
                    "status": 503}), 503)

    def put(self):
        try:
            now = datetime.now()
            body = request.data
            body = json.loads(body)
            short_url = body.get("short_url")
            redirect_url = body.get("redirect_url")
            try:
                with db.session() as session:
                    url = MdShortUrl.query.filter_by(short_url=short_url).first()
                    if not url:
                        return abort(404)

                    if url.valid_at < now:
                        return make_response(
                            jsonify({
                                "response": "Your ShortUrl is experired!",
                                "status": 403
                            }), 403)

                    valid_at = now + timedelta(days=5)
                    delta = valid_at - now
                    url.redirect_url = redirect_url
                    url.valid_at = valid_at
                    redis_client.set(short_url, redirect_url, ex=int(round(delta.total_seconds(), 0)))
                    session.commit()

                    return make_response(
                        jsonify({
                            "response": {
                                "message": "ShortUrl Updated with Sucessfully!!!",
                                "data": os.path.join(current_app.config["APP_DOMAIN"], short_url)
                            },
                            "status": 200
                        }), 200)

            except Exception as error:
                traceback.print_exc()
                session.rollback()
                return make_response(
                    jsonify({
                        "response": str(error),
                        "status": 503}), 503)

        except Exception as error:
            traceback.print_exc()
            return make_response(
                jsonify({
                    "response": str(error),
                    "status": 503}), 503)

    def delete(self):
        try:
            short_url = request.args.get("short_url")
            try:
                with db.session() as session:
                    url = MdShortUrl.query.filter_by(short_url=short_url).first()

                    if not url:
                        return abort(404)

                    session.delete(url)
                    session.commit()
                    return make_response(
                        jsonify({
                            "response": "ShortUrl deleted with sucessfully!!!",
                            "status": 200}), 200)

            except Exception as error:
                traceback.print_exc()
                session.rollback()
                return make_response(
                    jsonify({
                        "response": str(error),
                        "status": 503}), 503)

        except Exception as error:
            traceback.print_exc()
            return make_response(
                jsonify({
                    "response": str(error),
                    "status": 503}), 503)
