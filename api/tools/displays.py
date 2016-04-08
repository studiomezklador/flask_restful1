from simplexml import dumps
from flask import make_response, jsonify


def output_xml(data, status=200, headers=None):
    resp = make_response(dumps(dict(result=data)), status)
    resp.headers.extend(headers or {})
    return resp


def output_json(data, status=200, headers=None):
    resp = make_response(jsonify(result=data), status)
    resp.headers.extend(headers or {})
    return resp


def output_html(data, status=200, headers=None):
    resp = make_response(data, status)
    resp.headers.extend(headers or {})
    return resp
