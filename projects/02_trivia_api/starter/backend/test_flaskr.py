import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)
        self.db = None

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        pass

    def test_questions_get(self):
        qs = self.client().get("/questions")
        data = json.loads(qs.data)

        self.assertTrue(data)
        self.assertEqual(qs.status_code, 200)

    def test_questions_post(self):
        qs = self.client().post(
            "/questions?question='Foo'&answer='bar'&category='cats', difficulty=5"
        )

        self.assertEqual(qs.status_code, 200)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
