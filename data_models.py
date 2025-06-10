from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.String(10), nullable=True)
    date_of_death = db.Column(db.String(10), nullable=True)

    books = db.relationship('Book', backref='author', lazy=True)

    def __repr__(self):
        return f"<Author {self.id}: {self.name}>"

    def __str__(self):
        return self.name


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    publication_year = db.Column(db.String(4), nullable=True)  # e.g., "2020"
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

    def __repr__(self):
        return f"<Book {self.id}: {self.title} by Author ID {self.author_id}>"

    def __str__(self):
        return self.title
