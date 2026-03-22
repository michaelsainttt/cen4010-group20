from flask import Blueprint, jsonify, request
from database.supabase_client import supabase

wishlist_bp = Blueprint("wishlist", __name__)

@wishlist_bp.route("/wishlist", methods=["POST"])
def create_wishlist():
    data = request.get_json()
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    existing = supabase.table("wishlist").select("*").eq("user_id", user_id).execute()

    if len(existing.data) > 0:
        return jsonify({"error": "Wishlist already exists for this user"}), 400

    result = supabase.table("wishlist").insert({"user_id": user_id}).execute()

    return jsonify({
        "message": "Wishlist created",
        "data": result.data
    }), 201

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
