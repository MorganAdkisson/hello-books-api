from app import db
from app.models.book import Book
from flask import Blueprint, jsonify, make_response, request, abort

books_bp = Blueprint("books", __name__, url_prefix="/books")

@books_bp.route("", methods=["POST"])
def create_book():
    request_body = request.get_json()
    new_book = Book(title=request_body["title"],
        description=request_body["description"])
    db.session.add(new_book)
    db.session.commit()

    return make_response(f"Book {new_book.title} successfully created", 201)

@books_bp.route("", methods=["GET"])
def read_all_books(): 
    title_query = request.args.get("title")
    if title_query:
        books = Book.query.filter_by(title=title_query)
    else: 
        books = Book.query.all()
        
    books_response = []
    for book in books: 
        books_response.append({
            "id": book.id, 
            "title": book.title, 
            "description": book.description
        })

    return jsonify(books_response)

def validate_book(book_id):
    try: 
        book_id = int(book_id)
    except ValueError:
        abort(make_response({"message":f"book {book_id} invalid"}, 400))
    books = Book.query.all()
    for book in books: 
        if book.id == book_id:
            return book_id

    abort(make_response({"message": f"book {book_id} not found"}, 404))

@books_bp.route("/<book_id>", methods=["GET"])
def get_one_book(book_id):
    book = validate_book(book_id) 

    return {
        "id": book.id,
        "title": book.title, 
        "description": book.description
        }

@books_bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    book = validate_book(book_id)
    request_body = request.get_json()
    book.title = request_body["title"]
    book.description = request_body["description"]
    db.session.commit()

    return make_response(f"Book #{book_id} successfully updated")

@books_bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = validate_book(book_id)
    db.session.delete(book)
    db.session.commit()

    return make_response(f"Book #{book.id} sucessfully deleted")

hello_world_bp = Blueprint("hello_world", __name__)
@hello_world_bp.route("/hello-world", methods=["GET"]) 
def say_hello_world():
    my_beautiful_response_body = "Hello, World!"
    return my_beautiful_response_body

@hello_world_bp.route("/hello/JSON", methods=["GET"]) 
def say_hello_json():
    return {
        "name": "Ada Lovelace",
        "message": "Hello!",
        "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]        
    }

@hello_world_bp.route("/broken-endpoint-with-broken-server-code") 
def broken_endpoint(): 
    response_body = {
        "name": "Ada Lovelace", 
        "message": "Hello!", 
        "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
    }
    new_hobby = "Surfing"
    response_body["hobbies"] += [new_hobby]
    return response_body
