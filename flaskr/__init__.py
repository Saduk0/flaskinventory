import os

from flask import Flask

def create_app(test_config=None):
    # create the app
    app = Flask(__name__, instance_relative_config=True)
    # config the app
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
    # load instance config
        app.config.from_pyfile('config.py', silent=True)
    else:
    # load test config if passed
        app.config.from_mapping(test_config)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import admin
    app.register_blueprint(admin.bp)
    app.add_url_rule('/', endpoint='index')

    #simple page
    @app.route('/hello')
    def hello():
        return 'Hello'

    return app
