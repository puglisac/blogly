"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """user class"""

    def __repr__(self):
        """Show info about user."""

        u = self
        return f"<User {u.id} {u.first_name} {u.last_name}>"

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.Text,
                           nullable=False)
    last_name = db.Column(db.Text,
                          nullable=False)
    image_url = db.Column(db.Text)
    posts = db.relationship('Post', cascade="all, delete", backref="user")

    def update_user(self, first, last, img):
        """updates user info"""
        if first:
            self.first_name = first
        if last:
            self.last_name = last
        if img:
            self.image_url = img
        return

    @property
    def full_name(self):
        """returns full name of user"""
        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """post class"""

    def __repr__(self):
        """Show info about post."""

        p = self
        return f"<Post {p.id} {p.title}>"

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.Text,
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    created_at = db.Column(db.DateTime)
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tags = db.relationship('Tag',
                           secondary='posts_tags',
                           backref='posts')

    def update_post(self, title, content):
        """updates post info"""
        if title:
            self.title = title
        if content:
            self.content = content
        return

    def time_format(self):
        """returns a formated date and time"""
        dt = self.created_at
        return f"{dt.month}-{dt.day}-{dt.year} at {dt.strftime('%I:%M:%S %p')}"


def top_5_posts():
    joined = db.session.query(User, Post).join(Post)
    ordered = joined.order_by(db.desc(Post.created_at))
    return ordered.limit(5)


class Tag(db.Model):
    """tag class"""

    def __repr__(self):
        """Show info about tags."""

        t = self
        return f"<Tag {t.id} {t.name}>"

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.Text,
                     nullable=False)

    def update_tag(self, name):
        """updates tag name"""
        if name:
            self.name = name
        return


class PostTag(db.Model):
    """tag class"""

    def __repr__(self):
        """Show info about tags."""

        pt = self
        return f"<PostTag {pt.post_id} {pt.tag_id}>"

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer,
                        db.ForeignKey("posts.id"),
                        primary_key=True)
    tag_id = db.Column(db.Integer,
                       db.ForeignKey("tags.id"),
                       primary_key=True)
