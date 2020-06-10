import abc
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


# Base class for book endpoints
class BookEndpoint(Resource):
    @abc.abstractmethod
    def __init__(self):
        self.parser = reqparse.RequestParser()
        for field in ['title', 'author', 'isbn', 'category']:
            self.parser.add_argument(field, required=True)

class BookList(BookEndpoint):
    def get(self):
        shelf = get_db()
        keys = list(shelf.keys())
        books = [shelf[key] for key in keys]
        return books, 200

    def post(self):
        args = self.parser.parse_args()
        args['id'] = str(random.randint(1, 1000)) # bad way to assign id
        shelf = get_db()
        shelf[args['id']] = args
        return args, 201

class Book(BookEndpoint):
    def get(self, id):
        shelf = get_db()
        if not (id in shelf):
            return {}, 404
        else:
            return shelf[id], 200

    def put(self, id):
        shelf = get_db()
        if not (id in shelf):
            return {}, 404
        else:
            args = self.parser.parse_args()
            args['id'] = id
            shelf[id] = args
            return shelf[id], 200

    def delete(self, id):
        shelf = get_db()
        if not (id in shelf):
            return {}, 404
        else:
            del shelf[id]
            return {}, 204


# Register endpoints
api.add_resource(BookList, '/books')
api.add_resource(Book, '/book/<string:id>')


if __name__ == '__main__':
    app.run(debug=True)
