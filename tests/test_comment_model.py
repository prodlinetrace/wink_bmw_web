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

    def test_markdown(self):
        c = Comment()
        c.body = '# title\n\n## section\n\ntext **bold** and *italic*'
        self.assertTrue(c.body_html == '<h1>title</h1>\n<h2>section</h2>\n'
                        '<p>text <strong>bold</strong> '
                        'and <em>italic</em></p>')

    def test_notification_list(self):
        db.create_all()
        u1 = User(login='john', password='cat')
        u2 = User(login='susan', password='cat')
        p = Product(type=1234567890, serial=123456, week=45, year=15)
        c1 = Comment(body='comment body 1', author_id=u1.id, product_id=p.get_product_id())
        c2 = Comment(body='comment body 2', author_id=u1.id, product_id=p.get_product_id())
        c3 = Comment(body='comment body 3', author_id=u1.id, product_id=p.get_product_id())
        c4 = Comment(body='comment body 4', author_id=u1.id, product_id=p.get_product_id())
        c5 = Comment(body='comment body 5', author_id=u1.id, product_id=p.get_product_id())
        c6 = Comment(body='comment body 6', author_id=u1.id, product_id=p.get_product_id())
        
        db.session.add_all([u1, u2, p, c1, c2, c3, c4, c5])
        db.session.commit()
        """
        email_list = c4.notification_list()
        self.assertTrue(('e@e.com', 'n1') in email_list)
        self.assertFalse(('e2@e2.com', 'n2') in email_list)  # notify=False
        self.assertTrue(('susan@example.com', 'susan') in email_list)
        self.assertFalse(('e4@e4.com', 'n4') in email_list)  # comment author
        self.assertFalse(('e6@e6.com', 'n6') in email_list)
        email_list = c5.notification_list()
        self.assertFalse(('john@example.com', 'john') in email_list)
        self.assertTrue(('e4@e4.com', 'n4') in email_list)  # comment author
        """