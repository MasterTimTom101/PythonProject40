from flask import Flask, request, render_template, redirect, url_for, flash
from data_models import db, Author, Book
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, "data", "library.sqlite")

app = Flask(__name__)
app.secret_key = 'my_very_special_135238646_key'

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/library.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

"""
Uncomment this block the first time to create the tables
Then comment it again to avoid re-creating the DB each time
"""
with app.app_context():
   db.create_all()

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            new_author = Author(name=name)
            db.session.add(new_author)
            db.session.commit()
            flash('Author added successfully!', 'success')
            return redirect(url_for('add_author'))
    return render_template('add_author.html')

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    authors = Author.query.all()
    if request.method == 'POST':
        title = request.form.get('title')
        isbn = request.form.get('isbn')
        publication_year = request.form.get('publication_year')
        author_id = request.form.get('author_id')
        new_book = Book(title=title, isbn=isbn, publication_year=publication_year, author_id=author_id)
        db.session.add(new_book)
        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('add_book'))
    return render_template('add_book.html', authors=authors)

@app.route('/')
def home():
    search_query = request.args.get('search')
    if search_query:
        # Filter books by title or isbn
        books = Book.query.filter(
            (Book.title.ilike(f"%{search_query}%")) |
            (Book.isbn.ilike(f"%{search_query}%"))
        ).all()
    else:
        books = Book.query.all()

    """
    sort = request.args.get('sort', 'title')
    if sort == 'author':
        books = Book.query.join(Author).order_by(Author.name).all()
    else:
        books = Book.query.order_by(Book.title).all()
    """

    return render_template('home.html', books=books)


if __name__ == '__main__':
    app.run(host= "0.0.0.0", port = 5000, debug=True)
