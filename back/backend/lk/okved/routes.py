# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request
from flask import request, current_app as app
from flask import send_from_directory


# from flask.views import View
from models import db, OkvedCategory

import os
import json

bp = Blueprint(
    "okved",
    __name__,
)


@bp.route("/")
def index():
    return "okved hello!"


@bp.route("/list_category")
def list_category():

    cat_response: dict = {
        1: {},
        2: {},
        3: {},
    }

    def get_cat(name, desc):
        return {
            "Number": name,
            "CategoryName": desc,
            "Count": 1000,
            "Subcategories": [].copy(),
        }

    okved_categories = OkvedCategory.query.all()

    for okved_cat in okved_categories:
        cat_path = okved_cat.name.split(".")

        category = get_cat(okved_cat.name, str(cat.description).split("эта группи")[0])

        cat_response[len(cat_path)][okved_cat.name] = category

    for cat_name, cat in cat_response[3].items():
        path = cat_name.split(".")[:-1]

        try:
            cat_response[2][".".join(path)]["Subcategories"].append(cat)
        except KeyError:

            try:
                cat_response[1][".".join(path[:-1])]["Subcategories"].append(cat)
            except KeyError:
                cat_response[".".join(path[:-1])] = cat

    del cat_response[3]

    for cat_name, cat in cat_response[2].items():
        path = cat_name.split(".")[:-1]

        try:
            cat_response[1][".".join(path)]["Subcategories"].append(cat)
        except KeyError:
            cat_response[".".join(path[:-1])] = cat

    del cat_response[2]

    for cat_name, cat in cat_response[1].items():
        cat_response[cat_name] = cat

    del cat_response[1]
    del cat_response[""]

    return jsonify(list(cat_response.values()))


@bp.route("/search_category", methods=["GET", "POST"])
def search_category():
    def get_cat(name, desc):
        return {
            "Number": name,
            "CategoryName": desc,
            "Count": 1000,
            "Subcategories": [].copy(),
        }

    search_param = request.json.get("search", "").lower()

    okved_categories = OkvedCategory.query.filter(
        OkvedCategory.description.like(f"%{search_param}%")
    ).all()

    response: dict = []
    for cat in okved_categories:
        response.append(get_cat(cat.name, str(cat.description).split("эта группи")[0]))

    return jsonify(response)


@bp.route("/search_company", methods=["GET", "POST"])
def search_company():

    response: dict = {
        "heading": ["INN", "name", "site"],
        "body": [
            {"INN": "5020071841", "name": 'ООО "Экоагрофарминг"', "site": "mstuca.ru"},
            {
                "INN": "5003138045",
                "name": 'ООО "Агрохолдинг "Русрегионинвест"',
                "site": "",
            },
            {"INN": "5022053277 ", "name": 'ООО "Совхоз Проводник"', "site": ""},
        ],
    }

    return jsonify(response)


@bp.route("/worker/search/<path:path>", methods=["GET"])
def search(path):
    return send_from_directory("static/worker/search", path)

@bp.route("/worker/reporting/<path:path>", methods=["GET"])
def reporting(path):
    return send_from_directory("static/worker/reporting", path)

@bp.route("/manufactor/add/<path:path>", methods=["GET"])
def add(path):
    return send_from_directory("static/manufactor/add", path)

@bp.route("/manufactor/list/<path:path>", methods=["GET"])
def list(path):
    return send_from_directory("static/manufactor/list", path)