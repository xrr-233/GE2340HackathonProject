from flask import Flask

from apps.compute.view import compute_bp
from apps.index.view import index_bp

def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config['DEBUG'] = True
    app.register_blueprint(index_bp)
    app.register_blueprint(compute_bp)
    return app