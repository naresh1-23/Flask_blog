from flask_login import current_user
import email
from wsgiref.validate import validator
from flask import flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from sqlalchemy import DATE
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo
from post.models import User

class SigupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')
    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('Username already exist. Please choose another username')
    
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('Email already exist. Please choose another email')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class UpdateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Sign up')
    def validate_username(self, username):
        if username.data != current_user.username:    
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError('Username already exist. Please choose another username')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('Email already exist. Please choose another email')

class AddPost(FlaskForm):
    caption = StringField('Add Caption', validators=[DataRequired(),Length(min=2,max = 1000)])
    picture = FileField('Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Add Post')

