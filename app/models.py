from . import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    published_year = db.Column(db.String(20), nullable=True)
    notes = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "status": self.status,
            "rating": self.rating,
            "published_year": self.published_year,
            "notes": self.notes,
        }
