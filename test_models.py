from unittest import TestCase
from app import app
from models import db, User

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
    
    def tearDown(self):
        db.session.rollback()
    
    def test_update_user(self):
        user=User.query.get(self.user_id)
        user.update_user("Alan", "Puglisi","")
        self.assertEqual(user.first_name, "Alan")
        self.assertEqual(user.image_url, 'https://www.talkwalker.com/images/2020/blog-headers/image-analysis.png' )

    