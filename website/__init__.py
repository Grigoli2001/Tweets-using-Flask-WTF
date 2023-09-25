from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'qwerty'

    from .root import root
    app.register_blueprint(root,url_prefix='/')
    return app
