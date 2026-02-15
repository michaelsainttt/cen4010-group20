import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

app = Flask(__name__)

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_ROLE_KEY")
)

@app.get("/health")
def health():
    return {"status": "ok"}


#API TO FIND BOOK
@app.route("/books", methods=["GET"])
def only_title():
    response = supabase.table("books").select("*").execute()
    return jsonify(response.data)


#API TO SEE MORE DETAILS ABOUT BOOK VIA BOOK_ID
@app.route("/books/<int:book_id>", methods=["GET"])
def get_books_id(book_id):
    response = supabase.table("books").select("*").eq("id", book_id).execute()

    if len(response.data) == 0:
        return jsonify({"error": "Book Not Found"}),404
    return jsonify(response.data[0])

#API TO SEE BASED BOOKS ON GENRE
@app.route("/books/genre", methods=["GET"])
def get_books_genre():
    books_genre = request.args.get("genre")

    response = supabase.table("books").select("*").eq("genre",books_genre).execute()

    if len(response.data) == 0:
        return jsonify({"error": "Book Not Found"}),404
    return jsonify(response.data[0])

#TO SEE THE MINIMUM RATING
@app.route("/books/rating/float:min_rating>", methods=["GET"])
def books_by_rating(min_rating):
    response = supabase.table("books").select("*").gte("rating",min_rating).execute()

    if len(response.data) == 0:
        return jsonify({"error": "Book Not Found"})
    return jsonify(response.data)

#TO SEE THE TOP 10 MOST SOLD BOOKS
@app.route("/books/top10", methods=["GET"])
def top_10_books():
    response = supabase.table("books").select("*").order("copies_sold", ascending=False).limit(10).execute()

    return jsonify(response.data)


@app.route("/books/publisher-discount", methods=["PUT"])
def discount_books():
    publisher = request.args.get("publisher")
    discount_percent = request.args.get("discount_percent")

    if not publisher or discount_percent is None:
        return jsonify({"error": "publisher and discount_percent are required"}), 400

    try:
        discount_percent = float(discount_percent)
    except ValueError:
        return jsonify({"error": "discount_percent must be a number"}), 400

    if discount_percent <= 0:
        return jsonify({"error": "discount_percent must be > 0"}), 400

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

    return jsonify({"publisher": publisher, "discount_percent": discount_percent, "updated": len(books)}), 200

   
port = int(os.getenv("PORT", 5000))
app.run(host="0.0.0.0", port=port, debug=True)