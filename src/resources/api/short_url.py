# -*- coding: utf-8 -*-

import traceback
from flask_restful import Resource
from models.md_short_url import MdShortUrl
from flask import make_response, jsonify, request


class ShortUrlApi(Resource):
    def __init__(self, *args):
        ...

    def get(self):
        try:
            return make_response(
                jsonify({
                    "response": "GET",
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
            return make_response(
                jsonify({
                    "response": "POST",
                    "status": 201
                }), 201)
        except Exception as error:
            traceback.print_exc()
            return make_response(
                jsonify({
                    "response": str(error),
                    "status": 503}), 503)

    def put(self):
        try:
            return make_response(
                jsonify({
                    "response": "PUT",
                    "status": 200
                }), 200)
        except Exception as error:
            traceback.print_exc()
            return make_response(
                jsonify({
                    "response": str(error),
                    "status": 503}), 503)

    def delete(self):
        try:
            return make_response(
                jsonify({
                    "response": "DELETE",
                    "status": 200
                }), 200)
        except Exception as error:
            traceback.print_exc()
            return make_response(
                jsonify({
                    "response": str(error),
                    "status": 503}), 503)
