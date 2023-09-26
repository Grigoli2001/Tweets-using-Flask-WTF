import os
from flask import Blueprint, render_template,url_for, jsonify,g, request, redirect, flash, current_app
import sqlite3
from flask_login import login_required,current_user,logout_user
from .mongoDB import client
import datetime
from werkzeug.utils import secure_filename
from .forms import TweetForm
root = Blueprint('root',__name__)


@root.route('/')
def index():
    return render_template('home.html')
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
    return redirect(url_for('root.index'))

# Using MongoDB for tweets
db = client['tweets_db']
collection = db['tweets']
@root.route('/feed')
@login_required
def feed():
    try:
        tweets = list(collection.find())
        for tweet in tweets:
            tweet['_id'] = str(tweet['_id'])
        # return jsonify(tweets)
        return render_template('feed.html', tweets=tweets)
    except Exception:
        return "Error"



@root.route('/add_tweet', methods=[ 'GET','POST'])
@login_required
def addTweet():
    form = TweetForm()  # Create an instance of the TweetForm
    if form.validate_on_submit():        
        
        
        user_id = current_user.id
        content = form.content.data
        # Get the current timestamp
        today_date = datetime.date.today()
        created_at = today_date.strftime("%d %b %Y")

        image = form.image.data  # Get the uploaded image
        if not content and not image:
            flash('Please provide either content or an image.', 'danger')
            return render_template('add_tweet.html', form=form)
        # Check if an image was uploaded
        if image:
            image_filename = secure_filename(image.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename)
            image.save(image_path)
            
            # Save the image path in the database
            image_db_path = os.path.join('static', 'uploads', image_filename)  # Relative path for HTML
        else:
            image_db_path = None  # Handle the case where no image was uploaded

        tweet = {
            'content': content,
            'created_at': created_at,
            'updated_at': None,
            'user_id': user_id,
            'image_path': image_db_path  # Save the image path in the database
        }

        result = collection.insert_one(tweet)

        return redirect(url_for('root.feed'))

    return render_template('add_tweet.html',form = form)    



