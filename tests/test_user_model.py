import unittest
from app import create_app, db
from app.models import User, Product, Comment, load_user


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        #db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_user_loader(self):
        db.create_all()
        u = User(login='john', password='cat')
        db.session.add(u)
        db.session.commit()
        self.assertTrue(load_user(u.id) == u)

    def test_gravatar(self):
        u = User(login="john", password='cat')
        with self.app.test_request_context('/'):
            gravatar = u.gravatar()
            gravatar_256 = u.gravatar(size=256)
            gravatar_pg = u.gravatar(rating='pg')
            gravatar_retro = u.gravatar(default='retro')
        with self.app.test_request_context('/',
                                           base_url='https://example.com'):
            gravatar_ssl = u.gravatar()
        self.assertTrue('http://www.gravatar.com/avatar/' +
                        '527bd5b5d689e2c32ae974c6229ff785'in gravatar)
        self.assertTrue('s=256' in gravatar_256)
        self.assertTrue('r=pg' in gravatar_pg)
        self.assertTrue('d=retro' in gravatar_retro)
        self.assertTrue('https://secure.gravatar.com/avatar/' +
                        '527bd5b5d689e2c32ae974c6229ff785' in gravatar_ssl)

    def test_moderation(self):
        db.create_all()
        u1 = User(login='john', password='cat')
        u2 = User(login='susan', password='cat', is_admin=True)
        p = Product(type=1234567890, serial=123456, week=45, year=15)
        c1 = Comment(body='comment body 1', author_id=u1.id, product_id=p.get_product_id())
        c2 = Comment(body='comment body 2', author_id=u2.id, product_id=p.get_product_id())
        db.session.add_all([u1, u2, p, c1, c2])
        db.session.commit()
        """
        for_mod1 = u1.for_moderation().all()
        for_mod1_admin = u1.for_moderation(True).all()
        for_mod2 = u2.for_moderation().all()
        for_mod2_admin = u2.for_moderation(True).all()
        self.assertTrue(len(for_mod1) == 1)
        self.assertTrue(for_mod1[0] == c2)
        self.assertTrue(for_mod1_admin == for_mod1)
        self.assertTrue(len(for_mod2) == 0)
        self.assertTrue(len(for_mod2_admin) == 1)
        self.assertTrue(for_mod2_admin[0] == c2)
        """