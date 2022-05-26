from post import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email =  db.Column(db.String(120), unique= True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default = 'default.jpg')
    password = db.Column(db.String(1000), nullable = False)
    posts = db.relationship('Post', backref='author', lazy = True)
    like = db.relationship('Like', backref='author', lazy = True)
    comments = db.relationship('Comment', backref='commenter', lazy = True)
    def __repr__(self):
        return f"User('{ self.id }', '{ self.username }', '{ self.email }', '{ self.image_file }')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    caption = db.Column(db.String(1000), nullable = False)
    image_file = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_id = db.Column(db.Integer , db.ForeignKey('user.id'), nullable = False)
    like = db.relationship('Like', backref='poster', lazy = True)
    comments = db.relationship('Comment', backref='commentpost', lazy = True)

    def __repr__(self):
        return f"Post('{ self.id}','{ self.caption }','{ self.date_posted }' )"

class Like(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer , db.ForeignKey('user.id'), nullable = False)
    post_id = db.Column(db.Integer , db.ForeignKey('post.id'), nullable = False)

    def __repr__(self):
        return f"Like('{ self.id }','{ self.user_id }','{ self.post_id }' )"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    comment = db.Column(db.String(10000), nullable = False)
    user_id = db.Column(db.Integer , db.ForeignKey('user.id'), nullable = False)
    post_id = db.Column(db.Integer , db.ForeignKey('post.id'), nullable = False)

