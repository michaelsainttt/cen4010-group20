from flask import Blueprint, jsonify, request
from database.supabase_client import supabase

books_bp = Blueprint("books", __name__)


@books_bp.route("/books", methods=["GET"])
def only_title():
    response = supabase.table("books").select("*").execute()
    return jsonify(response.data)


@books_bp.route("/books/<int:book_id>", methods=["GET"])
def get_books_id(book_id):
    response = supabase.table("books").select("*").eq("id", book_id).execute()

    if len(response.data) == 0:
        return jsonify({"error": "Book Not Found"}), 404

    return jsonify(response.data[0])


@books_bp.route("/books/genre", methods=["GET"])
def get_books_genre():
    books_genre = request.args.get("genre")

    response = supabase.table("books").select("*").eq("genre", books_genre).execute()

    if len(response.data) == 0:
        return jsonify({"error": "Book Not Found"}), 404

    return jsonify(response.data)


@books_bp.route("/books/rating/<float:min_rating>", methods=["GET"])
def books_by_rating(min_rating):
    response = supabase.table("books").select("*").gte("rating", min_rating).execute()

    if len(response.data) == 0:
        return jsonify({"error": "Book Not Found"}), 404

    return jsonify(response.data)


@books_bp.route("/books/top10", methods=["GET"])
def top_10_books():
    response = (
        supabase
        .table("books")
        .select("*")
        .order("copies_sold", desc=True)
        .limit(10)
        .execute()
    )

    return jsonify(response.data)


@books_bp.route("/books/publisher-discount", methods=["PUT"])
def discount_books():
    publisher = request.args.get("publisher")
    discount_percent = request.args.get("discount_percent")

    if not publisher or discount_percent is None:
        return jsonify({"error": "publisher and discount_percent are required"}), 400

    try:
        discount_percent = float(discount_percent)
    except ValueError:
        return jsonify({"error": "discount_percent must be a number"}), 400

    books_response = supabase.table("books").select("id, price").eq("publisher", publisher).execute()
    books = books_response.data

    if len(books) == 0:
        return jsonify({"error": "No books found for that publisher"}), 404

    for book in books:
        new_price = round(float(book["price"]) * (1 - discount_percent / 100.0), 2)

        supabase.table("books").update({
            "discount_percent": discount_percent,
            "discounted_price": new_price
        }).eq("id", book["id"]).execute()

@books_bp.route("/books/discounted", methods=["GET"])
def get_discounted_books():

    response = supabase.table("books") \
        .select("*") \
        .gt("discount_percent", 0) \
        .execute()

    return jsonify(response.data)


# REMOVE DISCOUNT BY PUBLISHER
@books_bp.route("/books/remove-discount", methods=["PUT"])
def remove_discount():

    publisher = request.args.get("publisher")

    if not publisher:
        return jsonify({"error": "publisher is required"}), 400

    response = supabase.table("books") \
        .update({
            "discount_percent": None,
            "discounted_price": None
        }) \
        .eq("publisher", publisher) \
        .execute()

    return jsonify({
        "publisher": publisher,
        "updated_books": len(response.data)
    })


    return jsonify({
        "publisher": publisher,
        "discount_percent": discount_percent,
        "updated": len(books)
    }), 200