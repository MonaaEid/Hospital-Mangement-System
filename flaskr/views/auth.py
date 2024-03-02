import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from models import storage
from flaskr.views import app_views
from models.user import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@app_views.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        first_name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        # db = get_db()
        error = None

        if not first_name:
            error = 'name is required.'
        elif not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                data = {"first_name": first_name, "email": email, "password": password}
                instance = User(**data)
                instance.save()
            except:
                error = f"User {first_name} is already registered."
        else:
            return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


# @bp.route('/login', methods=('GET', 'POST'))
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         db = get_db()
#         error = None
#         user = db.execute(
#             'SELECT * FROM user WHERE username = ?', (username,)
#         ).fetchone()

#         if user is None:
#             error = 'Incorrect username.'
#         elif not check_password_hash(user['password'], password):
#             error = 'Incorrect password.'

#         if error is None:
#             session.clear()
#             session['user_id'] = user['id']
#             return redirect(url_for('index'))

#         flash(error)

#     return render_template('auth/login.html')


# @bp.before_app_request
# def load_logged_in_user():
#     user_id = session.get('user_id')

#     if user_id is None:
#         g.user = None
#     else:
#         g.user = get_db().execute(
#             'SELECT * FROM user WHERE id = ?', (user_id,)
#         ).fetchone()


# @bp.route('/logout')
# def logout():
#     session.clear()
#     return redirect(url_for('index'))


# def login_required(view):
#     @functools.wraps(view)
#     def wrapped_view(**kwargs):
#         if g.user is None:
#             return redirect(url_for('auth.login'))

#         return view(**kwargs)

#     return wrapped_view