from flask import Blueprint, jsonify, request
from database.supabase_client import supabase

book_details_bp = Blueprint("book_details", __name__)


# CREATE A BOOK
@book_details_bp.route("/book-details/books", methods=["POST"])
def create_book():
    data = request.get_json()

    isbn = data.get("isbn")
    book_name = data.get("book_name")
    description = data.get("description")
    price = data.get("price")
    author_id = data.get("author_id")
    genre = data.get("genre")
    publisher = data.get("publisher")
    year_published = data.get("year_published")
    copies_sold = data.get("copies_sold", 0)

    if not isbn or not book_name or not price or not author_id:
        return jsonify({"error": "isbn, book_name, price, and author_id are required"}), 400

    existing = supabase.table("books").select("id").eq("isbn", isbn).execute()
    if existing.data:
        return jsonify({"error": "A book with that ISBN already exists"}), 409

    response = supabase.table("books").insert({
        "isbn": isbn,
        "book_name": book_name,
        "description": description,
        "price": price,
        "author_id": author_id,
        "genre": genre,
        "publisher": publisher,
        "year_published": year_published,
        "copies_sold": copies_sold
    }).execute()

    return jsonify({
        "message": "Book created successfully",
        "book": response.data[0]
    }), 201


# GET A BOOK BY ISBN
@book_details_bp.route("/book-details/books/<string:isbn>", methods=["GET"])
def get_book_by_isbn(isbn):
    response = supabase.table("books").select("*").eq("isbn", isbn).execute()

    if len(response.data) == 0:
        return jsonify({"error": "Book not found"}), 404

    return jsonify(response.data[0]), 200


# CREATE AN AUTHOR
@book_details_bp.route("/book-details/authors", methods=["POST"])
def create_author():
    data = request.get_json()

    first_name = data.get("first_name")
    last_name = data.get("last_name")
    biography = data.get("biography")
    publisher = data.get("publisher")

    if not first_name or not last_name:
        return jsonify({"error": "first_name and last_name are required"}), 400

    response = supabase.table("authors").insert({
        "first_name": first_name,
        "last_name": last_name,
        "biography": biography,
        "publisher": publisher
    }).execute()

    return jsonify({
        "message": "Author created successfully",
        "author": response.data[0]
    }), 201


# GET ALL BOOKS BY AUTHOR ID
@book_details_bp.route("/book-details/authors/<int:author_id>/books", methods=["GET"])
def get_books_by_author(author_id):
    author_check = supabase.table("authors").select("id").eq("id", author_id).execute()
    if len(author_check.data) == 0:
        return jsonify({"error": "Author not found"}), 404

    response = supabase.table("books").select("*").eq("author_id", author_id).execute()

    if len(response.data) == 0:
        return jsonify({"error": "No books found for this author"}), 404

    return jsonify(response.data), 200
