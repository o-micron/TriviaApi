from flask import Flask, jsonify


def http_error(code: int, message: str, dictionary: dict = {}):
    dictionary.update({
        "status": code,
        "message": message,
        "success": False
    })
    return jsonify(dictionary), code


def http_error_500(dictionary: dict = {}):
    return http_error(500, "Internal Server Error", dictionary)


def http_error_405(dictionary: dict = {}):
    return http_error(405, "Method not found", dictionary)


def http_error_404(dictionary: dict = {}):
    return http_error(404, "Not found", dictionary)


def http_error_401(dictionary: dict = {}):
    return http_error(401, "Unauthorized", dictionary)


def http_error_400(dictionary: dict = {}):
    return http_error(400, "Bad request", dictionary)


def http_not_modified(dictionary: dict = {}):
    dictionary.update({
        "status": 304,
        "message": "Not modified",
        "success": True
    })
    return jsonify(dictionary), 304


def http_deleted(dictionary: dict = {}):
    dictionary.update({
        "status": 202,
        "message": "Deleted Successfully",
        "success": True
    })
    return jsonify(dictionary), 202


def http_created(dictionary: dict = {}):
    dictionary.update({
        "status": 201,
        "message": "Created Successfully",
        "success": True
    })
    return jsonify(dictionary), 201


def http_okay(dictionary: dict = {}):
    dictionary.update({
        "status": 200,
        "message": "OK",
        "success": True
    })
    return jsonify(dictionary), 200
