"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, top_5_posts, Tag, PostTag
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "some_secret_key"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)


@app.route("/")
def home_page():
    """displays the home page"""
    ordered_posts = top_5_posts()
    return render_template("home.html", posts=ordered_posts)


@app.route("/users")
def show_users():
    """shows a list of all users"""
    users = User.query.order_by(
        "last_name".lower(), "first_name".lower()).all()
    return render_template("users.html", users=users)


@app.route("/users/new")
def new_user():
    """shows a form to create a new user"""
    return render_template("new_user.html")


@app.route("/users/new", methods=["POST"])
def add_user():
    """adds the user to the database"""
    first = request.form["first"]
    last = request.form["last"]
    img = request.form["img"]
    new_user = User(first_name=first, last_name=last, image_url=img)
    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user_detail(user_id):
    """shows details about a users"""
    user = User.query.get_or_404(user_id)
    # posts = Post.query.filter(Post.poster_id==user_id)
    posts = user.posts
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
    first = request.form["first"]
    last = request.form["last"]
    img = request.form["img"]
    user.update_user(first, last, img)
    db.session.add(user)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """deletes a user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")


@app.route("/users/<int:user_id>/posts/new")
def show_post_form(user_id):
    """show form to create a new post"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("post_form.html", user=user, tags=tags)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    """adds a post"""
    title = request.form["title"]
    content = request.form["content"]
    tags_ids = [int(num) for num in request.form.getlist('tags')]
    tags= Tag.query.filter(Tag.id.in_(tags_ids)).all()
    new_post = Post(title=title, content=content,
                    poster_id=user_id, created_at=datetime.now(), tags=tags)

    db.session.add(new_post)
    db.session.commit()
    return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>")
def post_details(post_id):
    """shows post details"""
    post = Post.query.get_or_404(post_id)
    tags = post.tags
    return render_template("post_details.html", post=post, tags=tags)


@app.route("/posts/<int:post_id>/edit")
def edit_post_form(post_id):
    """shows post edit form"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template("edit_post.html", post=post, tags=tags)


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_posts(post_id):
    """deletes a post"""
    post = Post.query.get_or_404(post_id)
    user_id = post.user.id
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """edits post info"""
    post = Post.query.get_or_404(post_id)
    title = request.form["title"]
    content = request.form["content"]

    post.update_post(title, content)
    tags = [int(num) for num in request.form.getlist('tags')]
    post.tags = Tag.query.filter(Tag.id.in_(tags)).all()
    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post_id}")


@app.route("/tags")
def show_tags():
    """shows list of all tags"""
    tags = Tag.query.all()
    return render_template("tags.html", tags=tags)


@app.route("/tags/new")
def new_tag():
    """shows a form to create a new tag"""
    return render_template("new_tag.html")


@app.route("/tags/new", methods=["POST"])
def add_tag():
    """adds the tag to the database"""
    name = request.form["name"]

    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()
    return redirect("/tags")


@app.route("/tags/<int:tag_id>")
def tags_posts(tag_id):
    """shows posts associated with tags"""
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts
    return render_template("tag_posts.html", posts=posts, tag=tag)


@app.route("/tags/<int:tag_id>/edit")
def edit_tag_form(tag_id):
    """shows post edit form"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("edit_tag.html", tag=tag)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    """edits post info"""
    tag = Tag.query.get_or_404(tag_id)
    name = request.form["name"]

    tag.update_tag(name)
    db.session.add(tag)
    db.session.commit()

    return redirect(f"/tags/{tag_id}")


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """deletes a tag"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect(f"/tags")
