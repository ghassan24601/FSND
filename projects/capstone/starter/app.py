import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_cors import cross_origin

from models import Movies, Actors, setup_db
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    ## Error Handling
    """
    Example error handling for unprocessable entity
    """

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(404)
    def entity_not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "unprocessable"}),
            404,
        )

    @app.route("/actors", methods=["GET"])
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth(permission="get:actors")
    def actors():
        actors = Actors.query.all()
        return jsonify([actor.format() for actor in actors], 200)

    @app.route("/actors", methods=["POST"])
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth(permission="post:actors")
    def post_actors():
        name = request.args.get("name")
        age = request.args.get("age")
        new_actor = Actors(name=name, age=age)
        new_actor.insert()
        return jsonify(new_actor.format(), 200)

    @app.route("/actors/<int:actor_id>", methods=["GET"])
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth(permission="get:actors")
    def get_actor_by_id(actor_id):
        actor = Actors.query.get(actor_id).first()
        return jsonify(actor.format(), 200)

    @app.route("/actors/<int:actor_id>", methods=["DELETE"])
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth(permission="get:actors")
    def del_actor_by_id(actor_id):
        actor = Actors.query.get(actor_id).first()
        act = actor.format()
        actor.delete()
        return jsonify(act, 200)

    @app.route("/actors/<int:actor_id>", methods=["PATCH"])
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth(permission="patch:actors")
    def pat_actor_by_id(actor_id):
        actor = Actors.query.get(actor_id).first()
        name = request.args.get("name")
        age = request.args.get("age")
        actor.name = name
        actor.age = age
        actor.update()
        return jsonify(actor.format(), 200)

    @app.route("/movies", methods=["GET"])
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth(permission="get:movies")
    def get_movies():
        movies = Movies.query.all()
        return jsonify([movie.format() for movie in movies], 200)

    @app.route("/movies", methods=["POST"])
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth(permission="post:movies")
    def post_movies():
        title = request.args.get("title")
        release_date = request.args.get("release_date")
        new_movie = Movies(title=title, release_date=release_date)
        new_movie.insert()
        return jsonify(new_movie.format(), 200)

    @app.route("/movie/<int:movie_id>", methods=["GET"])
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth(permission="get:movies")
    def get_movie_by_id(movie_id):
        movie = Movies.query.get(movie_id).first()
        return jsonify(movie.format(), 200)

    @app.route("/movie/<int:movie_id>", methods=["PATCH"])
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth(permission="patch:movies")
    def movie_by_id(movie_id):
        movie = Movies.query.get(movie_id).first()
        title = request.args.get("title")
        release_date = request.args.get("release_date")
        movie.title = title
        movie.release_date = release_date
        movie.update()
        return jsonify(movie.format(), 200)

    @app.route("/movie/<int:movie_id>", methods=["DELETE"])
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth(permission="delete:movies"
    def movie_by_id(movie_id):
        movie = Movies.query.get(movie_id).first()
        mov = movie.format()
        movie.delete()
        return jsonify(mov, 200)

    return app


APP = create_app()
print(APP)

if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=8080, debug=True)
