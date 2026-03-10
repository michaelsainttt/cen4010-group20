import os
from flask import Flask
from dotenv import load_dotenv
from book.book_api import register_book_routes
from user.user_api import register_user_routes

load_dotenv()

app = Flask(__name__)

register_book_routes(app)
register_user_routes(app)

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)