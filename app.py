import os
from flask import Flask
from routes.books_routes import books_bp
from routes.wishlist_routes import wishlist_bp
from routes.user_routes import user_bp

app = Flask(__name__)

@app.get("/health")
def health():
    return {"status": "ok"}

app.register_blueprint(books_bp)
app.register_blueprint(wishlist_bp)
app.register_blueprint(user_bp)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)