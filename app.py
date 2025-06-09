from flask import Flask
from data_models import db
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, "data", "library.sqlite")

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/library.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

"""
Uncomment this block the first time to create the tables
Then comment it again to avoid re-creating the DB each time
"""
#with app.app_context():
#   db.create_all()


if __name__ == '__main__':
    app.run(host= "0.0.0.0", port = 5000, debug=True)
