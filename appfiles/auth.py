import functools

from flask import (
    Blueprint, current_app, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from appfiles.db import get_db

# Code template from https://flask.palletsprojects.com/en/2.3.x/tutorial/

# Create a blueprint for "auth"
bp = Blueprint('auth', __name__, url_prefix='/auth')

# Associate "/register" URL with the view function "register"
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            #with current_app.open_resource('schema.sql') as f:     
            #    db.cursor().executescript(f.read().decode('utf8')) 
                try:
                    db.execute(
                        "INSERT INTO user (username, password) VALUES (?, ?)",
                        (username, generate_password_hash(password)),
                    )
                    db.commit()
                except db.IntegrityError:
                    error = f"User {username} is already registered."
                else:
                    flash('Successfully registered')
                    return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


# Associate "/login" URL with the view function "login"
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            flash("Successfully logged in")
            return redirect(url_for('options.start_page'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    flash('You are logged out')
    return redirect(url_for('options.start_page'))
    #return render_template('auth/login.html')
    #return redirect(url_for('show_entries'))