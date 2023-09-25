from flask import Blueprint, render_template,url_for,session,redirect, request, flash
from flask_login import LoginManager, UserMixin, login_user,login_required,logout_user,current_user
from .root import show_users,conn_db,close_db
from . import create_app, login_manager
login_blueprint = Blueprint('login_blueprint',__name__)


class User(UserMixin):
    def __init__(self,id):
        self.id = id
        self.username = None
        self.email = None
        self.password = None    
        self.authenticated = False
    def is_active(self):
         return self.is_active()
    def is_anonymous(self):
         return False
    def is_authenticated(self):
         return self.authenticated
    def is_active(self):
         return True
    def get_id(self):
         return self.id
# with create_app().app_context():
#         # This context ensures that you can use Flask's session and other context-dependent features.
#         users = show_users()


@login_manager.user_loader
def load_user(user_id):
     # Fetch all user data from the database
    db = conn_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?',(user_id,))
    user = cursor.fetchone()
    if user[0] == user_id:
        cur_user = User(id=user_id)
        cur_user.username = user[1]
        cur_user.email = user[2]
        cur_user.password = user[3]
        return cur_user

    return None

@login_blueprint.route('/',methods = ['GET','POST'])
def login_logic():
    if current_user.is_authenticated:
         return redirect(url_for('root.profile'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = conn_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?',(email,))
        user = list(cursor.fetchone())
        if user:
            Us = load_user(user[0])
            if email == Us.email and password == Us.password:
                login_user(Us)
                return redirect(url_for('root.profile'))
            else:
                flash('Login Failed check your username and password','danger')
    return render_template('login.html')
 
