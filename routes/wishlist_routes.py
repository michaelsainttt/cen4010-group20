from flask import Blueprint, jsonify, request
from database.supabase_client import supabase

wishlist_bp = Blueprint("wishlist", __name__)

@wishlist_bp.route("/wishlist", methods=["POST"])
def create_wishlist():
    data = request.get_json()
    user_id = data.get("auth_user_id")

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    existing = supabase.table("wishlist").select("*").eq("auth_user_id", user_id).execute()

    if len(existing.data) > 0:
        return jsonify({"error": "Wishlist already exists for this user"}), 400

    result = supabase.table("wishlist").insert({"auth_user_id": user_id}).execute()

    return jsonify({
        "message": "Wishlist created",
        "data": result.data
    }), 201
