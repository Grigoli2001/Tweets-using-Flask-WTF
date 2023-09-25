from flask import Blueprint, render_template,url_for, jsonify,g, request, redirect,session, flash
import sqlite3
from flask_login import login_required,logout_user

root = Blueprint('root',__name__)


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
    
@root.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@root.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_blueprint.login_logic'))