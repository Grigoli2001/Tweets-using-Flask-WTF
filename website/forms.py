from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,TextAreaField,FileField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError



class RegistrationForm(FlaskForm):
    username=StringField("Username", validators=[DataRequired(),Length(min=2,max=20)])
    email=StringField("Email Address:", validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')


class TweetForm(FlaskForm):
    content = TextAreaField('Content', validators=[])
    image = FileField('Image')