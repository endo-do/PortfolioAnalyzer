from flask_login import login_required, current_user
from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route("/")
@login_required
def home():
    return render_template('home.html', user=current_user)