from flask import Blueprint, jsonify, request
from database.supabase_client import supabase

user_bp = Blueprint("user", __name__, url_prefix="/users")
# CREATE USER
@user_bp.route("", methods=["POST"])
def create_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    home_address = data.get("home_address")

    if not username or not password:
        return jsonify({"error": "username and password are required"}), 400

    existing_user = supabase.table("users").select("id").eq("username", username).execute()
    if existing_user.data:
        return jsonify({"error": "username already exists"}), 409

    response = supabase.table("users").insert({
        "auth_user_id": None,
        "username": username,
        "password" : password,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "home_address": home_address
     }).execute()

    return jsonify({
        "message": "user created successfully",
        "user": response.data[0]
    }), 201

# GET USER BY USERNAME
@user_bp.route("/<string:username>", methods=["GET"])
def get_user_by_username(username):
    response = supabase.table("users").select("*").eq("username", username).execute()

    if len(response.data) == 0:
        return jsonify({"error": "user not found"}), 404

    return jsonify(response.data[0]), 200

# UPDATE USER BY USERNAME
@user_bp.route("/<string:username>", methods=["PATCH"])
def update_user(username):
    data = request.get_json()

    if "email" in data:
        return jsonify({"error": "email cannot be updated"}), 400

    allowed_fields = {"first_name", "last_name", "home_address", "username"}
    update_data = {k: v for k, v in data.items() if k in allowed_fields}

    if not update_data:
        return jsonify({"error": "no valid fields provided"}), 400

    existing_user = supabase.table("users").select("*").eq("username", username).execute()
    if len(existing_user.data) == 0:
        return jsonify({"error": "user not found"}), 404

    if "username" in update_data and update_data["username"] != username:
        username_check = supabase.table("users").select("id").eq("username", update_data["username"]).execute()
        if username_check.data:
            return jsonify({"error": "new username already exists"}), 409

    response = supabase.table("users").update(update_data).eq("username", username).execute()

    return jsonify({
        "message": "user updated successfully",
        "user": response.data[0]
    }), 200

# CREATE CREDIT CARD FOR USER
@user_bp.route("/<string:username>/credit-cards", methods=["POST"])
def add_credit_card(username):
    data = request.get_json()

    card_holder_name = data.get("card_holder_name")
    card_number = data.get("card_number")
    expiration_month = data.get("expiration_month")
    expiration_year = data.get("expiration_year")
    billing_address = data.get("billing_address")

    if not card_holder_name or not card_number or not expiration_month or not expiration_year:
        return jsonify({"error": "missing required credit card fields"}), 400

    user_response = supabase.table("users").select("id").eq("username", username).execute()

    if len(user_response.data) == 0:
        return jsonify({"error": "user not found"}), 404

    user_id = user_response.data[0]["id"]

    last_four = card_number[-4:] if len(card_number) >= 4 else card_number

    response = supabase.table("credit_cards").insert({
        "user_id": user_id,
        "card_holder_name": card_holder_name,
        "card_number": card_number,
        "last_four": last_four,
        "expiration_month": expiration_month,
        "expiration_year": expiration_year,
        "billing_address": billing_address
    }).execute()

    return jsonify({
        "message": "credit card added successfully",
        "card": response.data[0]
    }), 201