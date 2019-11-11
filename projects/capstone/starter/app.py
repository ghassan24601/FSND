import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from .models import Movies, Actors

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)

  @app.route('/actors')
  def actors():
      actors = Actors.query.all()
      return jsonify([actor.format() for actor in actors])

  @app.route('/movies')
  def movies():
      movies = Movies.query.all()
      return jsonify([movie.format() for movie in movies])


  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)