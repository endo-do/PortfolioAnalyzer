from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from . import auth_bp
from ..db import get_db_connection, User
from flask_login import login_user, logout_user, login_required

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["userpwd"]
        password_confirm = request.form["userpwd_confirm"]

        if password != password_confirm:
            error = "Passwords do not match."
        else:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                error = "Username already exists."
            else:

                hashed_password = generate_password_hash(password)

                cursor.execute(
                    "INSERT INTO users (username, userpwd) VALUES (%s, %s)",
                    (username, hashed_password)
                )
                conn.commit()

                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                user_data = cursor.fetchone()

                cursor.close()
                conn.close()

                user = User(
                    user_data["userid"],
                    user_data["username"],
                    user_data["userpwd"]
                    )
                login_user(user)        
                return redirect(url_for("main.home"))

            cursor.close()
            conn.close()

    return render_template("register.html", error=error)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["userpwd"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user["userpwd"], password):
            user = User(
                    user_data["userid"],
                    user_data["username"],
                    user_data["userpwd"]
                    )
            login_user(user)        
            return redirect(url_for("main.home"))

        else:
            error = "Incorrect username or password"

    return render_template("login.html", error=error)

@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("auth.login"))