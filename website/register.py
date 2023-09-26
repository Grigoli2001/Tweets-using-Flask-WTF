from flask import Blueprint, render_template,url_for,session,redirect
import sqlite3
from .root import conn_db, authenticate_user
from .forms import RegistrationForm
register = Blueprint('register',__name__)

@register.route('/', methods = ['GET','POST'])
def add_user_form():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        try:
            db = conn_db()
            cursor = db.cursor()
            cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
            db.commit()
            user = authenticate_user(email, password)
            if user:
                # Store user data in the session
                session['user_id'] = user[0]
                session['user_username'] = user[1]
                return redirect(url_for('root.tweets'))
        except Exception as e:
            return str(e), 500
    return render_template('register.html',reg_form = form)




