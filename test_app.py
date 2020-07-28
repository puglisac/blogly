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

class App_Tests(TestCase):

    def setUp(self):
        User.query.delete()
        new_user=User(first_name='Joe', last_name='Smith', image_url='https://www.talkwalker.com/images/2020/blog-headers/image-analysis.png')
        db.session.add(new_user)
        db.session.commit()
        self.user_id=new_user.id
    def tearDown(self):
        db.session.rollback()

    def test_root(self):
        with app.test_client() as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Users</h2>', html)

    def test_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Joe Smith', html)

    def test_create_user(self):
        with app.test_client() as client:
            user_info={"first": "Alan", "last":"Puglisi", "img":""}
            resp = client.post("/users/new", data=user_info, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Alan Puglisi', html)

    def test_edit_user(self):
        with app.test_client() as client:
            user_info={"first": "Alan", "last":"Puglisi", "img":""}
            resp = client.post(f"/users/{self.user_id}/edit", data=user_info, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Alan Puglisi', html)

    def test_delete(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Joe Smith', html)