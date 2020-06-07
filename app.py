import random
import shelve

from flask import Flask, g
from flask_restful import Resource, Api, reqparse


# Creating flask and api instances
app = Flask(__name__)
api = Api(app)


# DB handling pattern per flask docs
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("books")
    return db

@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# Books Endpoint
class BookList(Resource):
    def get(self):
        shelf = get_db()
        keys = list(shelf.keys())
        books = [shelf[key] for key in keys]
        return books, 200

    def post(self):
        parser = reqparse.RequestParser()
        fields = ['title', 'author', 'isbn', 'category']
        for field in fields:
            parser.add_argument(field, required=True)
        args = parser.parse_args()
        args['id'] = str(random.randint(1, 1_000_000)) # bad way to assign id
        shelf = get_db()
        shelf[args['id']] = args
        return args, 201

api.add_resource(BookList, '/books')


if __name__ == '__main__':
    app.run(debug=True)
