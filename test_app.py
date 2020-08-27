from unittest import TestCase
from app import app
from models import db, User, Post, Tag, PostTag
from datetime import datetime

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

        Tag.query.delete()
        new_tag=Tag(name='tag name')
        db.session.add(new_tag)
        db.session.commit()
        self.tag_id=new_tag.id

        Post.query.delete()
        new_post=Post(title='post title', content='post content', poster_id=self.user_id, created_at=datetime.now())
        db.session.add(new_post)
        db.session.commit()
        self.post_id=new_post.id


    def tearDown(self):
        db.session.rollback()
        Post.query.delete()
        Tag.query.delete()
        db.session.commit()

    def test_root(self):
        with app.test_client() as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<div class="mb-2">', html)

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
            resp = client.post(f"/users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Joe Smith', html)

    def test_post_details(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('post title', html)

    def test_new_post(self):
        with app.test_client() as client:
            post_info={"title": "new title", "content":"new content"}
            resp = client.post(f"/users/{self.user_id}/posts/new", data=post_info, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('new title', html)

    def test_edit_post(self):
        with app.test_client() as client:
            post_info={"title": "newer title", "content":"newer content"}
            resp = client.post(f"/posts/{self.post_id}/edit", data=post_info, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('newer title', html)
    
    def test_delete_post(self):
        with app.test_client() as client:
            post_info={"title": "gone title", "content":"gone content"}
            resp = client.post(f"/posts/{self.post_id}/delete", data=post_info, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('gone title', html)

    def test_tags(self):
        with app.test_client() as client:
            resp = client.get(f"/tags")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('tag name', html)

    # def test_tag_posts(self):
    #     with app.test_client() as client:
    #         new_user=User(first_name='bob', last_name='jo', image_url='https://www.talkwalker.com/images/2020/blog-headers/image-analysis.png')
    #         db.session.add(new_user)
    #         db.session.commit()
    #         print(new_user)
    #         new_post=Post(title='new title', content='new content', poster_id=new_user.id, created_at=datetime.now())
    #         tag=Tag.query.get(self.tag_id)
    #         print("tag: ", tag)
    #         new_post.tags.append(tag)
    #         db.session.add(new_post)
    #         db.session.commit()
    #         resp = client.get(f"/tags/{self.tag_id}")
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn('tag name', html)

    def test_new_tag(self):
        with app.test_client() as client:
            resp = client.post(f"/tags/new", data={"name":"new name"}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('new name', html)
    
    def test_delete_tag(self):
        with app.test_client() as client:
            resp = client.post(f"/tags/{self.tag_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('tag name', html)