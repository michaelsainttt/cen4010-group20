import os
from flask import Flask, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

BOOKS = [
    {
        "id": 1,
        "title": "Don Quixote",
        "author": "Miguel de Cervantes",
        "description": "A man becomes obsessed with chivalry and becomes a knight.",
        "genre": "Classic",
        "rating": 4.0,
        "price": 12.99
    },
    {
        "id": 2,
        "title": "1984",
        "author": "George Orwell",
        "description": "A dystopian novel about surveillance and totalitarian control.",
        "genre": "Dystopian",
        "rating": 4.7,
        "price": 9.99
    },
    {
        "id": 3,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "description": "A story of wealth, love, and tragedy in the 1920s.",
        "genre": "Classic",
        "rating": 4.3,
        "price": 10.99
    },
    {
        "id": 4,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "description": "A novel about justice and racism in the American South.",
        "genre": "Fiction",
        "rating": 4.8,
        "price": 8.99
    },
    {
        "id": 5,
        "title": "Moby-Dick",
        "author": "Herman Melville",
        "description": "A captain’s obsession with hunting a giant white whale.",
        "genre": "Adventure",
        "rating": 3.9,
        "price": 14.99
    },
    {
        "id": 6,
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "description": "A romantic novel about manners, class, and misunderstandings.",
        "genre": "Romance",
        "rating": 4.6,
        "price": 7.99
    },
    {
        "id": 7,
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "description": "A fantasy adventure about a hobbit joining a quest for treasure.",
        "genre": "Fantasy",
        "rating": 4.8,
        "price": 11.49
    },
    {
        "id": 8,
        "title": "Harry Potter and the Sorcerer's Stone",
        "author": "J.K. Rowling",
        "description": "A boy discovers he is a wizard and attends Hogwarts School.",
        "genre": "Fantasy",
        "rating": 4.9,
        "price": 8.49
    },
    {
        "id": 9,
        "title": "The Catcher in the Rye",
        "author": "J.D. Salinger",
        "description": "A teenager struggles with identity and growing up.",
        "genre": "Fiction",
        "rating": 4.0,
        "price": 6.99
    },
    {
        "id": 10,
        "title": "The Book Thief",
        "author": "Markus Zusak",
        "description": "A girl in Nazi Germany finds comfort in stealing books.",
        "genre": "Historical Fiction",
        "rating": 4.7,
        "price": 12.49
    },
    {
        "id": 11,
        "title": "Sapiens",
        "author": "Yuval Noah Harari",
        "description": "A history of humankind from the Stone Age to today.",
        "genre": "Nonfiction",
        "rating": 4.7,
        "price": 16.99
    },
    {
        "id": 12,
        "title": "The Art of War",
        "author": "Sun Tzu",
        "description": "An ancient guide to military strategy and leadership.",
        "genre": "Philosophy",
        "rating": 4.4,
        "price": 5.99
    },
    {
        "id": 13,
        "title": "The Road",
        "author": "Cormac McCarthy",
        "description": "A father and son survive in a bleak post-apocalyptic world.",
        "genre": "Post-Apocalyptic",
        "rating": 4.1,
        "price": 13.99
    },
    {
        "id": 14,
        "title": "Dune",
        "author": "Frank Herbert",
        "description": "A sci-fi epic about politics, power, and survival on a desert planet.",
        "genre": "Science Fiction",
        "rating": 4.6,
        "price": 10.99
    },
    {
        "id": 15,
        "title": "The Hunger Games",
        "author": "Suzanne Collins",
        "description": "A girl fights to survive in a deadly televised competition.",
        "genre": "Dystopian",
        "rating": 4.5,
        "price": 9.49
    }

]

@app.get("/health")
def health():
    return {"status": "ok"}


#API TO FIND BOOK
@app.route("/books", methods=["GET"])
def only_title():
    title_only = []
    for book in BOOKS:
        #ONLY DISPLAYS THE TITLE AND ID OF THE BOOK 
        title_only.append({
            "id": book["id"],
            "title": book["title"]
        })

    return jsonify(title_only)


#API TO SEE MORE DETAILS ABOUT BOOK VIA BOOK_ID
@app.route("/books/<int:book_id>", methods=["GET"])
def get_books_id(book_id):
    for book in BOOKS:
        if book["id"] == book_id:
            return jsonify(book)
    return jsonify({"error": "Book Not Found"}), 404 #RETURN ERROR IF BOOK NOT FOUND 

@app.route("/books/genre", methods=["GET"])
def get_books_genre(books_genre):
    for book in BOOKS:
        if book["genre"] == books_genre:
            return jsonify(book)
    return jsonify({"error": "Book Not Found"}), 404

@app.route("/books/<int:rating>", methods=["GET"])
def get_book_rating(rating):
    

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
