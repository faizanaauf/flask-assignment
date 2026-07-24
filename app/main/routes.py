from flask import render_template, request, redirect, url_for, flash, session

from .. import db
from ..models import Book
from . import main

STATUSES = ["Want to Read", "Reading", "Finished"]


def _get_genres():
    genres = [row[0] for row in db.session.query(Book.genre).distinct().order_by(Book.genre).all()]
    return genres


@main.route("/")
def index():
    genre_filter = session.get("genre_filter")
    if genre_filter:
        books = Book.query.filter_by(genre=genre_filter).order_by(Book.title).all()
    else:
        books = Book.query.order_by(Book.title).all()

    genres = _get_genres()
    return render_template(
        "index.html",
        books=books,
        selected_genre=genre_filter,
        genres=genres,
        statuses=STATUSES,
    )


@main.route("/filter", methods=["POST"])
def set_filter():
    genre = request.form.get("genre", "").strip()
    if genre:
        session["genre_filter"] = genre
        flash(f"Genre filter saved: {genre}", "info")
    else:
        session.pop("genre_filter", None)
        flash("Genre filter cleared.", "info")
    return redirect(url_for("main.index"))


@main.route("/books/create", methods=["GET", "POST"])
def create_book():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        genre = request.form.get("genre", "").strip()
        status = request.form.get("status", "").strip()
        rating = request.form.get("rating", "").strip()
        published_year = request.form.get("published_year", "").strip()
        notes = request.form.get("notes", "").strip()

        errors = []
        if not title:
            errors.append("Title is required.")
        if not author:
            errors.append("Author is required.")
        if not genre:
            errors.append("Genre is required.")
        if status not in STATUSES:
            errors.append("Status is invalid.")
        try:
            rating_value = int(rating)
            if rating_value < 1 or rating_value > 5:
                errors.append("Rating must be between 1 and 5.")
        except ValueError:
            errors.append("Rating must be an integer between 1 and 5.")

        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template(
                "create.html",
                statuses=STATUSES,
                genres=_get_genres(),
                form_data=request.form,
            )

        book = Book(
            title=title,
            author=author,
            genre=genre,
            status=status,
            rating=rating_value,
            published_year=published_year or None,
            notes=notes or None,
        )
        db.session.add(book)
        db.session.commit()
        flash("Book added successfully.", "success")
        return redirect(url_for("main.index"))

    return render_template("create.html", statuses=STATUSES, genres=_get_genres(), form_data={})


@main.route("/books/<int:book_id>/edit", methods=["GET", "POST"])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        genre = request.form.get("genre", "").strip()
        status = request.form.get("status", "").strip()
        rating = request.form.get("rating", "").strip()
        published_year = request.form.get("published_year", "").strip()
        notes = request.form.get("notes", "").strip()

        errors = []
        if not title:
            errors.append("Title is required.")
        if not author:
            errors.append("Author is required.")
        if not genre:
            errors.append("Genre is required.")
        if status not in STATUSES:
            errors.append("Status is invalid.")
        try:
            rating_value = int(rating)
            if rating_value < 1 or rating_value > 5:
                errors.append("Rating must be between 1 and 5.")
        except ValueError:
            errors.append("Rating must be an integer between 1 and 5.")

        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template(
                "edit.html",
                statuses=STATUSES,
                genres=_get_genres(),
                book=book,
                form_data=request.form,
            )

        book.title = title
        book.author = author
        book.genre = genre
        book.status = status
        book.rating = rating_value
        book.published_year = published_year or None
        book.notes = notes or None
        db.session.commit()
        flash("Book updated successfully.", "success")
        return redirect(url_for("main.index"))

    return render_template("edit.html", statuses=STATUSES, genres=_get_genres(), book=book, form_data={})


@main.route("/books/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash("Book deleted successfully.", "success")
    return redirect(url_for("main.index"))
