from flask import Blueprint, jsonify, request
from database.supabase_client import supabase

wishlist_bp = Blueprint("wishlist", __name__)


@wishlist_bp.route("/wishlist/<int:user_id>", methods=["GET"])
def get_wishlist(user_id):

    result = supabase.table("wishlist").select("*").eq("user_id", user_id).execute()

    if len(result.data) == 0:
        return jsonify({"error": "Wishlist not found"}), 404

    return jsonify(result.data), 200

@wishlist_bp.route("/wishlist/<int:user_id>", methods=["DELETE"])
def delete_wishlist(user_id):

    result = supabase.table("wishlist").delete().eq("user_id", user_id).execute()

    return jsonify({
        "message": "Wishlist deleted",
        "deleted": len(result.data)
    }), 200

@wishlist_bp.route("/wishlist", methods=["POST"])
def add_to_wishlist():
    data = request.get_json()

    user_id = data.get("user_id")
    book_id = data.get("book_id")

    if not user_id or not book_id:
        return jsonify({"error": "user_id and book_id are required"}), 400


    existing = supabase.table("wishlist").select("*") \
    .eq("user_id", user_id) \
    .eq("book_id", book_id) \
    .execute()

    if existing.data:
        return jsonify({"message": "Book already in wishlist"}), 200


    response = supabase.table("wishlist").insert({
        "user_id": user_id,
        "book_id": book_id
    }).execute()

    return jsonify({
        "message": "Book added to wishlist",
        "data": response.data
    }), 201
