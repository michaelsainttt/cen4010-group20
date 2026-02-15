import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

app = Flask(__name__)

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_ANON_KEY")
)

@app.get("/health")
def health():
    return {"status": "ok"}


#API TO FIND BOOK
@app.route("/books", methods=["GET"])
def only_title():
    response = supabase.table("books").select("id, title").execute()
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
@app.route("/books/<float:min_rating>", methods=["GET"])
def books_by_rating(min_rating):
    response = supabase.table("books").select("*").gte("rating",min_rating).execute()

    if len(response.data) == 0:
        return jsonify({"error": "Book Not Found"})
    return jsonify(response.data)

#TO SEE THE TOP 10 MOST SOLD BOOKS


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)