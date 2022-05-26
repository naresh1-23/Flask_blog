from fileinput import filename
import secrets
import os
from PIL import Image
from post import app, db , bcrypt
from flask import flash, redirect, render_template, request , url_for
from post import form
from post.form import AddPost, SigupForm, LoginForm, UpdateForm
from post.models import User , Post, Like, Comment
from flask_login import login_user, current_user, logout_user

@app.route('/', methods = ['GET', 'POST'])
@app.route('/home', methods = ['GET', 'POST'])
def home():
    posts  = Post.query.order_by(Post.date_posted.desc())
    like = Like
    if request.method == 'POST':
        post = request.form.get("caption")
        likepost(post)
    return render_template('home.html', title = 'Home',  posts = posts, like = like)


def likepost(post):
    posting = Post.query.filter_by(id = post).first()
    likes = Like.query.filter_by(author = current_user ,poster = posting).first()
    if likes:
        db.session.delete(likes)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        liking = Like(author = current_user ,poster = posting)
        db.session.add(liking)
        db.session.commit()
        return redirect(url_for('home'))
    
@app.route('/home/comment/<int:post_id>', methods = ['GET', 'POST'])
def comment(post_id):
    if current_user.is_authenticated:
        image_file = url_for('static', filename='pp/'+current_user.image_file)
        post = Post.query.filter_by( id = post_id).first()
        coment = Comment()
        if request.method == 'POST':
            comments = request.form.get('comment')
            commentpush(post, comments)
        return render_template('comment.html',coment = coment, post = post, image_file  = image_file)
    else:
        return redirect(url_for('login'))

def commentpush(post, comments):
    posts = post
    commenting  = comments
    coment = Comment(comment = commenting, commenter = current_user, commentpost = posts)
    db.session.add(coment)
    db.session.commit()

@app.route('/profile')
def profile():
    if current_user.is_authenticated:
        image_file = url_for('static', filename='pp/'+current_user.image_file)
        return render_template('profile.html', title = 'Profile', image_file = image_file )
    else:
        flash(f'First Log in', 'warning')
        return redirect(url_for('login'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name , f_ext = os.path.splitext( form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/pp', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form= SigupForm()
    if form.validate_on_submit():
        if form.picture.data:
            pic_name = save_picture(form.picture.data)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, image_file = pic_name, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Signup', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form= LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by( username= form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash(f'welcome { user.username }', 'success')
            login_user(user)
            return redirect(url_for('profile'))
        else:
            flash(f'Username and password did not matched', 'warning')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/update', methods = ['GET', 'POST'])
def update():
    form= UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            pic_name = save_picture(form.picture.data)
        else:
            pic_name = current_user.image_file
        current_user.image_file = pic_name
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Your profile has been successfully updated', 'success')
        return redirect(url_for('profile'))
    return render_template('update.html', title='Signup', form=form)

def save_post(form_picture):
    random_hex = secrets.token_hex(8)
    f_name , f_ext = os.path.splitext( form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/post', picture_fn)
    output_size = (1000, 1000)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/addpost', methods = ['GET', 'POST'])
def addpost():
    form  = AddPost()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            if form.picture.data:
                pic_name = save_post(form.picture.data)
            post = Post(caption = form.caption.data, image_file = pic_name, author = current_user)
            db.session.add(post)
            db.session.commit()
            flash(f"Your post is successfully posted!!",'success')
            return render_template('addpost.html', title = 'Add Post', form = form)
    else:
        flash(f'First Log in', 'warning')
        return redirect(url_for('login'))
    return render_template('addpost.html', title = 'Add Post', form = form)


@app.route('/users')  
def Users():
    users = User
    return render_template('user.html', users = users)