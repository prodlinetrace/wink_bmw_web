import unittest
from app import create_app, db
from app.models import User, Product, Comment


class CommentModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        #db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_approved(self):
        db.create_all()
        u = User(login='john', password='cat')
        p = Product(type=1234567890, serial=123456, week=45, year=15)
        c1 = Comment(body='comment body 1', author_id=u.id, product_id=p.get_product_id())
        c2 = Comment(body='comment body 2', author_id=u.id, product_id=p.get_product_id())
        db.session.add_all([u, p, c1, c2])
        db.session.commit()
        comments = p.comments.all()
        self.assertTrue(len(comments) == 2)
        self.assertTrue(comments[0] == c1)

