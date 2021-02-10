import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# create the app
app = Flask(__name__, instance_relative_config=True)
# config the app
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    SQLALCHEMY_DATABASE_URI='sqlite:///flaskr.db',
)
db = SQLAlchemy(app)

from . import models
# models.init_models()

# from . import db
# db.init_app(app)

from . import auth
app.register_blueprint(auth.bp)

from . import inventory
app.register_blueprint(inventory.bp)
app.add_url_rule('/', endpoint='index')

#simple page
@app.route('/hello')
def hello():
    return 'Hello'
