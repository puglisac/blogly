from models import db, User, Post
from app import app

db.drop_all()
db.create_all()

u1 = User(first_name="Alan", last_name="Puglisi", image_url="")
u2 = User(first_name="Alli", last_name="Havlik", image_url="https://helpx.adobe.com/content/dam/help/en/stock/how-to/visual-reverse-image-search-v2_297x176.jpg")

db.session.add(u1)
db.session.add(u2)
db.session.commit()