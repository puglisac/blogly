"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "some_secret_key"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route("/")
def home_page():
    """displays the home page"""
    return redirect("/users")

@app.route("/users")
def show_users():
    """shows a list of all users"""
    users=User.query.order_by("last_name".lower(), "first_name".lower()).all()
    return render_template("users.html", users=users)

@app.route("/users/new")
def new_user():
    """shows a form to create a new user"""
    return render_template("new_user.html")

@app.route("/users/new", methods=["POST"])
def add_user():
    """adds the user to the database"""
    first=request.form["first"]
    last=request.form["last"]
    img=request.form["img"]
    new_user=User(first_name=first, last_name=last, image_url=img)
    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:user_id>")
def show_user_detail(user_id):
    """shows details about a users"""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.poster_id==user_id)
    print("post:= ",posts)
    return render_template("user_detail.html", user=user, posts=posts)

@app.route("/users/<int:user_id>/edit")
def show_edit_form(user_id):
    """shows a form to edit user info"""
    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """edits user info"""
    user = User.query.get_or_404(user_id)
    first=request.form["first"]
    last=request.form["last"]
    img=request.form["img"]
    user.update_user(first, last, img)
    db.session.add(user)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route("/users/<int:user_id>/delete")
def delete_user(user_id):
    """deletes a user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:user_id>/posts/new")
def show_post_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("post_form.html", user=user)
    
@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    """adds a post"""
    title=request.form["title"]
    content=request.form["content"]
    new_post=Post(title=title, content=content, poster_id=user_id, created_at=datetime.now())
    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")