from flask import jsonify, request

from .. import db
from ..models import Book
from . import api


def _validate_book_payload(payload):
    errors = []
    title = payload.get("title", "").strip()
    author = payload.get("author", "").strip()
    genre = payload.get("genre", "").strip()
    status = payload.get("status", "").strip()
    rating = payload.get("rating")

    if not title:
        errors.append("Title is required.")
    if not author:
        errors.append("Author is required.")
    if not genre:
        errors.append("Genre is required.")
    if status not in ["Want to Read", "Reading", "Finished"]:
        errors.append("Status must be one of Want to Read, Reading, Finished.")
    try:
        rating_value = int(rating)
        if rating_value < 1 or rating_value > 5:
            errors.append("Rating must be between 1 and 5.")
    except (TypeError, ValueError):
        errors.append("Rating must be an integer between 1 and 5.")

    return errors


@api.route("/books", methods=["GET"])
def get_books():
    books = Book.query.order_by(Book.title).all()
    return jsonify([book.to_dict() for book in books]), 200


@api.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return jsonify({"error": "Book not found."}), 404
    return jsonify(book.to_dict()), 200


@api.route("/books", methods=["POST"])
def create_book_api():
    payload = request.get_json() or {}
    errors = _validate_book_payload(payload)
    if errors:
        return jsonify({"errors": errors}), 400

    book = Book(
        title=payload["title"].strip(),
        author=payload["author"].strip(),
        genre=payload["genre"].strip(),
        status=payload["status"].strip(),
        rating=int(payload["rating"]),
        published_year=payload.get("published_year", "") or None,
        notes=payload.get("notes", "") or None,
    )
    db.session.add(book)
    db.session.commit()
    return jsonify(book.to_dict()), 201


@api.route("/books/<int:book_id>", methods=["PUT"])
def update_book_api(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return jsonify({"error": "Book not found."}), 404

    payload = request.get_json() or {}
    errors = _validate_book_payload(payload)
    if errors:
        return jsonify({"errors": errors}), 400

    book.title = payload["title"].strip()
    book.author = payload["author"].strip()
    book.genre = payload["genre"].strip()
    book.status = payload["status"].strip()
    book.rating = int(payload["rating"])
    book.published_year = payload.get("published_year", "") or None
    book.notes = payload.get("notes", "") or None
    db.session.commit()
    return jsonify(book.to_dict()), 200


@api.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book_api(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return jsonify({"error": "Book not found."}), 404

    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted."}), 200
