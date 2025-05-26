"""Handles the authentication routes"""


from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from . import auth_bp
from app.database.connection import User, get_db_connection, release_db_connection
from flask_login import login_user, logout_user, login_required


# register route
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    error = None
    
    if request.method == "POST":
        
        # get data from register form
        username = request.form["username"]
        password = request.form["userpwd"]
        password_confirm = request.form["userpwd_confirm"]

        if password != password_confirm:
            error = "Passwords do not match."
        
        else:
            # check for already existing user
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                error = "Username already exists."
            
            else:
                # hash password and insert new user into db
                hashed_password = generate_password_hash(password)
                cursor.execute(
                    "INSERT INTO users (username, userpwd) VALUES (%s, %s)",
                    (username, hashed_password)
                )
                conn.commit()

    	        # get new user data
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                user_data = cursor.fetchone()
                cursor.close()
                conn.close()
                user = User(
                    user_data["userid"],
                    user_data["username"],
                    user_data["userpwd"]
                    )
                
                # login user and redirect to main page
                login_user(user)        
                return redirect(url_for("main.home"))

            cursor.close()
            conn.close()
            release_db_connection(conn)

    return render_template("register.html", error=error)


# login route
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    
    if request.method == "POST":
        # get data from login form
        username = request.form["username"]
        password = request.form["userpwd"]

        # check if user exists in db
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user_data = cursor.fetchone()
        cursor.close()
        release_db_connection(conn)

        if user_data and check_password_hash(user_data["userpwd"], password):
            # login user if details match
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


# logout
@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("auth.login"))