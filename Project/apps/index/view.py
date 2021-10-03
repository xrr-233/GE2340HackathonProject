from flask import Blueprint, render_template

index_bp = Blueprint('login', __name__)

@index_bp.route('/')
def render_earth():
    return render_template('index/index.html')