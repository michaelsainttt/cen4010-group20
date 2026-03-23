from flask import Blueprint, jsonify, request
from database.supabase_client import supabase

wishlist_bp = Blueprint("wishlist", __name__)


@wishlist_bp.route("/wishlist/<int:wishlist_id>", methods=["GET"])
def get_wishlist(wishlist_id):

    result = supabase.table("wishlist").select("*").eq("wishlist_id", wishlist_id).execute()

    if len(result.data) == 0:
        return jsonify({"error": "Wishlist not found"}), 404

    return jsonify(result.data), 200

@wishlist_bp.route("/wishlist/remove", methods=["DELETE"])
def remove_book():
    data = request.get_json()

    wishlist_id = data.get("wishlist_id")
    book_id = data.get("book_id")

    if not wishlist_id or not book_id:
        return jsonify({"error": "wishlist_id and book_id required"}), 400

    result = supabase.table("wishlist") \
        .delete() \
        .eq("wishlist_id", wishlist_id) \
        .eq("book_id", book_id) \
        .execute()

    return jsonify({
        "message": "Book removed",
        "deleted": len(result.data)
    }), 200

@wishlist_bp.route("/wishlist", methods=["POST"])
def add_to_wishlist():
    data = request.get_json()

    user_id = data.get("user_id")
    name = data.get("name")
    book_id = data.get("book_id")
    wishlist_id = data.get("wishlist_id")

    if user_id and name:
        existing = supabase.table("wishlist").select("*") \
            .eq("user_id", user_id) \
            .eq("name", name) \
            .execute()

        if existing.data:
            return jsonify({"error": "Wishlist name already exists"}), 400

        import time
        new_wishlist_id = int(time.time())

        result = supabase.table("wishlist").insert({
            "user_id": user_id,
            "wishlist_id": new_wishlist_id,
            "name": name
        }).execute()

        return jsonify({
            "message": "Wishlist created",
            "wishlist_id": new_wishlist_id,
            "data": result.data
        }), 201


    if wishlist_id and book_id:
        existing = supabase.table("wishlist").select("*") \
            .eq("wishlist_id", wishlist_id) \
            .eq("book_id", book_id) \
            .execute()

        if existing.data:
            return jsonify({"message": "Book already in wishlist"}), 200

        result = supabase.table("wishlist").insert({
            "wishlist_id": wishlist_id,
            "book_id": book_id,
            "user_id": user_id
        }).execute()

        return jsonify({
            "message": "Book added to wishlist",
            "data": result.data
        }), 201

    return jsonify({"error": "Invalid request"}), 400
