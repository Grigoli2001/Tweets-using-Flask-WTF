from flask import Blueprint, render_template,url_for, jsonify,g, request, redirect,session
import sqlite3
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
root = Blueprint('root',__name__)


class RegistrationForm(FlaskForm):
    username=StringField("Username", validators=[DataRequired(),Length(min=2,max=20)])
    email=StringField("Email Address:", validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')
@root.route('/')
def index():
    return "Heyy"
def conn_db():
    db = getattr(g,'_database',None)
    if db is None:
        db = g._database = sqlite3.connect('user_data.db')
        create_user_table(db)
    
    return db
        
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Create a table if it doesn't exist
def create_user_table(db):
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password text NOT NULL
        )
    ''')
    db.commit()

@root.route('/add_user', methods=['POST'])
def add_user():

    try:
        db = conn_db()
        cursor = db.cursor()
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
        db.commit()
        user = authenticate_user(email, password)
        if user:
            # Store user data in the session
            session['user_id'] = user[0]
            session['user_username'] = user[1]

            return redirect(url_for('root.notes'))

        
    except Exception as e:
        return str(e), 500

@root.route('/register', methods = ['GET','POST'])
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
                return redirect(url_for('root.reg_suc'))
        except Exception as e:
            return str(e), 500
    return render_template('register.html',form = form)



@root.route('/reg-suc')
def reg_suc():
    return 'Registration Successful'


@root.route('/users')
def show_users():
    # Fetch all user data from the database
    db = conn_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()

    # Pass the user data to the template
    return jsonify(users)

def authenticate_user(email, password):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cursor.fetchone()
    conn.close()
    if user and user[3] == password:  # Check if the password matches
        return user
    else:
        return None
    

@root.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('root.notes'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = authenticate_user(email, password)

        if user:
            # Store user data in the session
            session['user_id'] = user[0]
            session['user_username'] = user[1]
            return redirect(url_for('root.notes'))
        else:
            error = 'Invalid email or password'
            return render_template('login.html', error=error)

    return render_template('login.html')

@root.route('/logout')
def logout():
    session.pop('user_id',None)
    return redirect(url_for('root.login'))
