from flask import Blueprint, jsonify, request
from database.supabase_client import supabase

cart_bp = Blueprint("cart_bp", __name__)

@cart_bp.route("/cart/<int:user_id>", methods=["GET"])
def get_cart(user_id):
    response = supabase.table("shopping_cart") \
        .select("*") \
        .eq("user_id", user_id) \
        .execute()
    return jsonify(response.data)

@cart_bp.route("/cart/add", methods=["POST"])
def add_to_cart():
    data = request.json

    user_id = data["user_id"]
    book_id = data["book_id"]

    supabase.table("shopping_cart").insert({
        "user_id": user_id,
        "book_id": book_id
    }).execute()

    return jsonify({"message": "Book added to cart"})

@cart_bp.route("/cart/remove", methods=["DELETE"])
def remove_from_cart():
    data = request.json

    user_id = data["user_id"]
    book_id = data["book_id"]

    supabase.table("shopping_cart") \
        .delete() \
        .eq("user_id", user_id) \
        .eq("book_id", book_id) \
        .execute()

    return jsonify({"message": "Book removed from cart"})

@cart_bp.route("/cart/subtotal/<int:user_id>", methods=["GET"])
def cart_subtotal(user_id):
    cart_items = supabase.table("shopping_cart") \
        .select("book_id") \
        .eq("user_id", user_id) \
        .execute()

    subtotal = 0

    for item in cart_items.data:
        book = supabase.table("books") \
            .select("price") \
            .eq("id", item["book_id"]) \
            .execute()

        if len(book.data) > 0:
            subtotal += float(book.data[0]["price"])

    return jsonify({"user_id": user_id, "subtotal": subtotal})
#shopping cart update