import os

from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        #DATABASE="webtext.db"
        DATABASE=os.path.join(app.instance_path, 'appfiles.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    
    # Import and call the init-app function defined in db.py
    from . import db
    db.init_app(app)

    # Register authentication blueprint - for login, registration etc.
    from . import auth
    app.register_blueprint(auth.bp)

    # Register options blueprint
    from . import options
    app.register_blueprint(options.bp)
    app.add_url_rule('/', endpoint='index')


    return app
