from flask_sqlalchemy import SQLAlchemy

# here the database object
db = SQLAlchemy()

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.String(10))  # format: YYYY-MM-DD
    date_of_death = db.Column(db.String(10))  # format: YYYY-MM-DD

    books = db.relationship('Book', backref='author', lazy=True)

    def __repr__(self):
        return f"<Author {self.name}>"

    def __str__(self):
        return self.name


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    publication_year = db.Column(db.String(4))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

    """
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "isbn" : self.isbn,
            "author_id" : self.author_id,
            "publication_year" : self.publication_year
        }
    """

    def __repr__(self):
        return f"<Book {self.title}>"

    def __str__(self):
        return self.title
