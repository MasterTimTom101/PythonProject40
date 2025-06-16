from flask import Flask, request, render_template, redirect, url_for, flash
from data_models import db, Author, Book
import os
from datetime import datetime



BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, "data", "library.sqlite")

app = Flask(__name__)
app.secret_key = 'my_very_special_135238646_key'

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
"""
Uncomment this block the first time to create the tables
Then comment it again to avoid re-creating the DB each time
"""
#with app.app_context():
#   db.create_all()


@app.route('/')
def home():
    """
    This is the initial start page of the application app.py
    It shows the sorted list of all books...sorted by title
    Gives back the page 'home.html' and transfers the variable
     'books'
    """
    sort = request.args.get('sort', 'title')
    if sort == 'author':
        books = Book.query.join(Author).order_by(Author.name).all()
    if sort == 'title':
        books = Book.query.order_by(Book.title).all()
    search_query = request.args.get('search')
    if search_query:
        # Filter books by title
        books = Book.query.filter(
            (Book.title.ilike(f"%{search_query}%"))
        ).all()
    return render_template('home.html', books=books)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    This is the entry route of the 'add_author' page of
    the application app.py. Adds author only if not already exists
    It shows the input mask to add an author with or without
    date of birth and with or without date of death
    Gives back the page 'add_author.html'
    """
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        # Check if author is already existing
        existing_author = Author.query.filter(
            db.func.lower(Author.name) == name.lower()
        ).first()
        if existing_author:
            flash(f'Author "{name}" already exists.', 'warning')
        else:
            new_author = Author(name=name)
            db.session.add(new_author)
            db.session.commit()
            flash(f'Author "{name}" added successfully!', 'success')
            return redirect(url_for('add_author'))
    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    This is the entry route of the 'add_book' page of the
    application app.py
    It shows the input mask to add a book.
    Adds a book only if the isbn is unique.
    Gives back the page 'add_book.html' and transfers
     the variable 'authors'
    """
    authors = Author.query.all()
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        isbn = request.form.get('isbn', '').strip()
        publication_year = request.form.get('publication_year', '').strip()
        author_id = request.form.get('author_id')
        if not title or not isbn or not author_id:
            flash('Title, ISBN, and Author are required fields.', 'danger')
            return redirect(url_for('add_book'))
        # Check if isbn is already existing
        existing_book = Book.query.filter_by(isbn=isbn).first()
        if existing_book:
            flash(f'A book with ISBN "{isbn}" already exists.', 'warning')
        else:
            new_book = Book(
                title=title,
                isbn=isbn,
                publication_year=publication_year,
                author_id=author_id
            )
            db.session.add(new_book)
            db.session.commit()
            flash(f'Book "{title}" added successfully!', 'success')
            return redirect(url_for('add_book'))
    return render_template('add_book.html', authors=authors)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """
    This is the entry route of the 'delete a book' page of the
    application app.py
    It shows the input mask to delete a book.
    Gives back (redirects) to the page 'home.html'
    """
    book = Book.query.get_or_404(book_id)
    author = Author.query.get(book.author_id)
    # Delete the book
    db.session.delete(book)
    db.session.commit()
    # Check if the author has any other books left
    other_books = Book.query.filter_by(author_id=author.id).count()
    if other_books == 0:
        db.session.delete(author)
        db.session.commit()
        flash(f'Book and author "{author.name}" were deleted successfully!', 'success')
    else:
        flash(f'Book "{book.title}" was deleted successfully!', 'success')
    return redirect(url_for('home'))


if __name__ == '__main__':
    """
    if app.py is called directly then the flask task 
    will be executed other way not executed.
    The host will be on any local address on port 5000 
    The debug flag is on True
    """
    app.run(host= "0.0.0.0", port = 5000, debug=True)
