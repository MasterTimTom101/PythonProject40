from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):
    """
    Defines the Author data model:
    - id: Unique identifier for each author (primary key)
    - name: Name of the author (required)
    - birth_date: Optional birth date of the author (as string, e.g., 'YYYY-MM-DD')
    - date_of_death: Optional death date as a string like birth date
    - books: One-to-many relationship to Book model (one author is able to write many books)
    """
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
    """
    Defines the Book data model:
    - id: Unique identifier for each book (primary key)
    - isbn: Unique ISBN number (required)
    - title: Title of the book (required)
    - publication_year: Optional year of publication (as string, e.g., '2020')
    - author_id: Foreign key linking to an author (required)
    """
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20), nullable=False, unique = True)
    title = db.Column(db.String(200), nullable=False)
    publication_year = db.Column(db.String(4), nullable=True)  # e.g., "2020"
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

    def __repr__(self):
        return f"<Book {self.id}: {self.title} by Author ID {self.author_id}>"

    def __str__(self):
        return self.title
