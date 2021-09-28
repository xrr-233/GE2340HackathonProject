from flask import Flask

from apps.index.view import index_bp


def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.register_blueprint(index_bp)
    return app