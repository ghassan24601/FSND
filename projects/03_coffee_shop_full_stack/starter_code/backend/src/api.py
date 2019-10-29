import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)


"""
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
"""
db_drop_and_create_all()

d = Drink(title="Old Fashioned", recipe="Mix a bunch of stuff together")

d.insert()


## ROUTES


@app.route("/drinks", methods=["GET", "POST"])
@requires_auth(permission="post:drinks")
def drinks():
    if request.method == "GET":
        drinks = Drink.query.all()
        return jsonify({"success": True, "drinks": [d.short() for d in drinks]}), 200
    else:
        drink = Drink(
            title=request.args.get("title"), recipe=request.args.get("recipe")
        )
        drink.insert()
        return jsonify({"success": True, "drinks": drink.short()})


@app.route("/drinks-detail")
@requires_auth(permission="get:drinks-detail")
def drinks_detail():
    drinks = Drink.query.all()
    return jsonify({"success": True, "drinks": [d.long() for d in drinks]}), 200


@app.route("/drinks/<int:drink_id>")
@requires_auth(permission="patch:drinks")
def update_drink(drink_id):
    drink = Drink.query.get(drink_id).first()
    drink.title = request.args.get("title")
    drink.recipe = request.args.get("recipe")
    drink.update()
    return jsonify({"success": True, "drinks": [d.long for d in drink]}), 200


@app.route("/drinks/<int:drink_id")
@requires_auth(permission="delete:drinks")
def update_drink(drink_id):
    try:
        drink = Drink.query.get(drink_id).first()
    except exc.DBAPIError:
        abort(404)
    drink.delete()
    return jsonify({"success": True, "delete": drink_id}), 200


## Error Handling
"""
Example error handling for unprocessable entity
"""


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({"success": False, "error": 422, "message": "unprocessable"}), 422


@app.errorhandler(404)
def entity_not_found(error):
    return jsonify({"success": False, "error": 404, "message": "unprocessable"}), 404
