
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    publisher = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"{self.book_name} - {self.author}"
    
# GET: Retrieve all books
@app.route("/books", methods=["GET"])
def get_books():
    books = Book.query.all()

    output = []

    for book in books:
        book_data = {
            "id": book.id,
            "book_name": book.book_name,
            "author": book.author,
            "publisher": book.publisher
        }

        output.append(book_data)

    return {"books": output}

# GET: Retrieve one book by ID
@app.route("/books/<int:id>", methods=["GET"])
def get_book(id):
    book = db.session.get(Book, id)

    if book is None:
        return {"error": "Book not found"}, 404

    return {
        "id": book.id,
        "book_name": book.book_name,
        "author": book.author,
        "publisher": book.publisher
    }

# POST: Add a new book
@app.route("/books", methods=["POST"])
def add_book():
    new_book = Book(
        book_name=request.json["book_name"],
        author=request.json["author"],
        publisher=request.json["publisher"]
    )

    db.session.add(new_book)
    db.session.commit()

    return {"id": new_book.id}

# DELETE: Remove a book by ID
@app.route("/books/<int:id>", methods=["DELETE"])
def delete_book(id):
    book = db.session.get(Book, id)

    if book is None:
        return {"error": "Book not found"}, 404

    db.session.delete(book)
    db.session.commit()

    return {"message": "Book successfully deleted"}

# PUT: Update an existing book
@app.route("/books/<int:id>", methods=["PUT"])
def update_book(id):
    book = db.session.get(Book, id)

    if book is None:
        return {"error": "Book not found"}, 404

    data = request.get_json()

    book.book_name = data["book_name"]
    book.author = data["author"]
    book.publisher = data["publisher"]

    db.session.commit()

    return {"message": "Book successfully updated"}

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
