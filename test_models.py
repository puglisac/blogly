from unittest import TestCase
from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogy_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING']=True
app.config['DEBUT_TB_HOSTS']=['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class Model_Tests(TestCase):

    def setUp(self):
        User.query.delete()
        new_user=User(first_name='Joe', last_name='Smith', image_url='https://www.talkwalker.com/images/2020/blog-headers/image-analysis.png')
        db.session.add(new_user)
        db.session.commit()
        
        self.user_id=new_user.id

        Post.query.delete()
        new_post=Post(title='post title', content='post content', poster_id=self.user_id)
        db.session.add(new_post)
        db.session.commit()

        self.post_id=new_post.id

    def tearDown(self):
        db.session.rollback()
        Post.query.delete()
        db.session.commit()
    
    def test_user_class(self):
        user=User.query.get(self.user_id)
        self.assertEqual(user.first_name, "Joe")
    
    def test_update_user(self):
        user=User.query.get(self.user_id)
        user.update_user("Alan", "Puglisi","")
        self.assertEqual(user.first_name, "Alan")
        self.assertEqual(user.image_url, 'https://www.talkwalker.com/images/2020/blog-headers/image-analysis.png' )

    def test_post(self):

        post=Post.query.get(self.post_id)
        self.assertEqual(post.title, 'post title')