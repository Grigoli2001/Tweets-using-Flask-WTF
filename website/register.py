from flask import Blueprint, render_template,url_for,session,redirect
import sqlite3
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from .root import conn_db, authenticate_user
register = Blueprint('register',__name__)

class RegistrationForm(FlaskForm):
    username=StringField("Username", validators=[DataRequired(),Length(min=2,max=20)])
    email=StringField("Email Address:", validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')

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
                return redirect(url_for('register.reg_suc'))
        except Exception as e:
            return str(e), 500
    return render_template('register.html',form = form)



@register.route('/reg-suc')
def reg_suc():
    return 'Registration Successful'

