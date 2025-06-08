```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    published_date = db.Column(db.String(10), nullable=False)

    def __init__(self, title, author, published_date):
        self.title = title
        self.author = author
        self.published_date = published_date

class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book
        load_instance = True

    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    published_date = fields.Str(required=True)

book_schema = BookSchema()
books_schema = BookSchema(many=True)

@app.route('/books', methods=['POST'])
def add_book():
    try:
        book_data = book_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_book = Book(title=book_data.title, author=book_data.author, published_date=book_data.published_date)
    db.session.add(new_book)
    db.session.commit()
    return book_schema.jsonify(new_book), 201

@app.route('/books', methods=['GET'])
def get_books():
    all_books = Book.query.all()
    return books_schema.jsonify(all_books)

@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id)
    return book_schema.jsonify(book)

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get_or_404(id)
    try:
        book_data = book_schema.load(request.json, instance=book, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    db.session.commit()
    return book_schema.jsonify(book)

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
```