from flask_login import login_required, current_user
from flask import Blueprint, render_template
from .db import get_db_connection

bp = Blueprint('main', __name__)

@bp.route("/")
@login_required
def home():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.callproc("get_user_portfolios_with_values", (current_user.id,))
    portfolios = []
    for result in cursor.stored_results():
        portfolios.extend(result.fetchall())

    cursor.close()
    conn.close()

    return render_template('home.html', user=current_user, portfolios=portfolios)