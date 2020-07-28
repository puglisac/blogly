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
    posts = db.relationship('Post', cascade="all, delete-orphan")
    

    def update_user(self, first, last, img):
        """updates user info"""
        if first:
            self.first_name=first
        if last:
            self.last_name=last
        if img:
            self.image_url=img
    
    @property
    def full_name(self):
        """returns full name of user"""
        return f"{self.first_name} {self.last_name}"

class Post(db.Model):
    """post class"""
    def __repr__(self):
        """Show info about post."""

        p = self
        return f"<Post {u.id} {u.first_name} {u.last_name}>"

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
    user = db.relationship('User')

    def update_post(self, title, content):
        """updates post info"""
        if title:
            self.title=title
        if content:
            self.content=content
    
    def time_format(self):
        """returns a formated date and time"""
        dt=self.created_at
        return f"{dt.month}-{dt.day}-{dt.year} at {dt.strftime('%I:%M:%S %p')}"

    