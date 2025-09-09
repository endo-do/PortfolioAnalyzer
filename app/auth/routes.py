"""Handles the authentication routes"""


from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from . import auth_bp
from app.database.connection.user import User
from app.database.helpers.execute_change_query import execute_change_query
from app.database.helpers.fetch_one import fetch_one
from flask_login import login_user, logout_user, login_required
from app.utils.password_validator import validate_password_strength, generate_password_requirements_text
from app.utils.logger import log_user_action, log_security_event, log_error


# register route
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    
    if request.method == 'POST':
        try:
            # get data from register form
            username = request.form.get('username', '').strip()
            password = request.form.get('userpwd', '')
            password_confirm = request.form.get('userpwd_confirm', '')

            # Input validation
            if not username:
                error = 'Username is required.'
            elif len(username) < 3:
                error = 'Username must be at least 3 characters long.'
            elif len(username) > 50:
                error = 'Username must be 50 characters or less.'
            elif not password:
                error = 'Password is required.'
            elif password != password_confirm:
                error = 'Passwords do not match.'
            else:
                # Advanced password validation
                is_valid, password_errors, strength, score = validate_password_strength(password, username)
                if not is_valid:
                    error = f"Password requirements not met: {'; '.join(password_errors)}"
                elif score < 40:  # Require at least medium strength
                    error = f"Password is too weak (strength: {strength}). Please choose a stronger password."
                else:
                    # check for already existing user
                    existing_user = fetch_one('SELECT * FROM user WHERE username = %s', (username,))

                    if existing_user:
                        error = 'Username already exists.'
                        log_security_event('REGISTRATION_ATTEMPT_DUPLICATE', f'Attempted to register with existing username: {username}')
                    else:
                        # hash password and insert new user into db
                        hashed_password = generate_password_hash(password)
                        execute_change_query(
                            'INSERT INTO user (username, userpwd, email, default_base_currency) VALUES (%s, %s, %s, %s)',
                            (username, hashed_password, 'N/A', 1)
                        )

                        # get new user data
                        user_data = fetch_one('SELECT * FROM user WHERE username = %s', (username,), dictionary=True)
                        if user_data:
                            user = User(
                                user_data['userid'],
                                user_data['username'],
                                user_data['userpwd'],
                                user_data.get('email', 'N/A'),
                                user_data.get('default_base_currency', 1),
                                user_data['is_admin']
                            )
                            
                            # Log successful registration
                            log_user_action('USER_REGISTERED', {
                                'username': username,
                                'password_strength': strength,
                                'password_score': score
                            })
                            
                            # login user and redirect to main page
                            login_user(user)        
                            return redirect(url_for('main.home'))
                        else:
                            error = 'Registration failed. Please try again.'

        except Exception as e:
            log_error(e, {'action': 'user_registration', 'username': username})
            error = f'An error occurred during registration: {str(e)}'

    return render_template('register.html', error=error, password_requirements=generate_password_requirements_text())


# login route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    
    if request.method == 'POST':
        try:
            # get data from login form
            username = request.form.get('username', '').strip()
            password = request.form.get('userpwd', '')

            # Input validation
            if not username:
                error = 'Username is required.'
            elif not password:
                error = 'Password is required.'
            else:
                # check if user exists in db
                user_data = fetch_one('SELECT * FROM user WHERE username = %s', (username,), dictionary=True)

                if user_data and check_password_hash(user_data['userpwd'], password):
                    # login user if details match
                    user = User(
                            user_data['userid'],
                            user_data['username'],
                            user_data['userpwd'],
                            user_data.get('email', 'N/A'),
                            user_data.get('default_base_currency', 1),
                            user_data['is_admin']
                            )
                    
                    # Log successful login
                    log_user_action('USER_LOGIN', {'username': username})
                    
                    login_user(user)        
                    return redirect(url_for('main.home'))
                else:
                    error = 'Incorrect username or password'
                    # Log failed login attempt
                    log_security_event('LOGIN_FAILED', f'Failed login attempt for username: {username}')

        except Exception as e:
            log_error(e, {'action': 'user_login', 'username': username})
            error = f'An error occurred during login: {str(e)}'

    return render_template('login.html', error=error)


# logout
@auth_bp.route('/logout')
@login_required
def logout():
    # Log logout action
    log_user_action('USER_LOGOUT')
    logout_user()
    flash('Logged out.')
    return redirect(url_for('auth.login'))