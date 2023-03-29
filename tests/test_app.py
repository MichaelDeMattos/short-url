# -*- coding: utf-8 -*-

import sys
import os
import json
import random
import os.path
import requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

host = "165.232.154.205:5000"

def test_fetch_short_url():
    """ Consumer Rest API /api/short_url with Methods [GET, POST, PUT, DELETE] """

    # Create ShortUrl's with 6 or 10 chars
    short_urls = []
    for size, redirect_url in [[5, "http://google.com"], [6, "http://youtube.com"], [7, "http://github.com"], [8, "http://facebook.com"], [9, "http://twitter.com"], [10, "http://twitch.tv"]]:
        req = requests.post(
            f"http://{host}/api/short_url",
            data=json.dumps({
                "redirect_url": redirect_url,
                "size": size
            }),
            timeout=60)
        resp = req.json()
        assert req.status_code == 201
        assert type(resp) == dict
        short_urls.append(resp.get("response").get("data").split("http://")[1].split("/")[1])

    # Get ShortUrl's
    for short_url in short_urls:
        req = requests.get(
            f"http://{host}/api/short_url",
            params={"short_url": short_url},
            timeout=60)

        resp = req.json()
        assert req.status_code == 200
        assert type(resp) == dict

    # Update Short's
    for short_url in short_urls:
        req = requests.put(
            f"http://{host}/api/short_url",
            data=json.dumps({
                "short_url": short_url,
                "redirect_url": "https://dotpyc.com"}),
            timeout=60)

        resp = req.json()
        assert req.status_code == 200
        assert type(resp) == dict

    # Get ShortUrl's again
    for short_url in short_urls:
        req = requests.get(
            f"http://{host}/api/short_url",
            params={"short_url": short_url},
            timeout=60)

        resp = req.json()
        assert req.status_code == 200
        assert type(resp) == dict

    # Delete Short's
    for short_url in short_urls:
        req = requests.delete(
            f"http://{host}/api/short_url",
            params={"short_url": short_url},
            timeout=60)

        resp = req.json()
        assert req.status_code == 200
        assert type(resp) == dict

    # Get ShortUrl's again
    for short_url in short_urls:
        req = requests.get(
            f"http://{host}/api/short_url",
            params={"short_url": short_url},
            timeout=60)

        resp = req.json()
        assert req.status_code == 503
        assert type(resp) == dict
