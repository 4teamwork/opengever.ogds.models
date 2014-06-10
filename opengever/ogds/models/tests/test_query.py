from opengever.ogds.models.testing import DATABASE_LAYER
from opengever.ogds.models.user import User
from sqlalchemy.orm.exc import NoResultFound
import unittest2


class TestQueryBase(unittest2.TestCase):

    layer = DATABASE_LAYER

    @property
    def session(self):
        return self.layer.session

    def setUp(self):
        super(TestQueryBase, self).setUp()
        self.john = User('john')
        self.hugo = User('hugo')
        self.session.add(self.john)
        self.session.add(self.hugo)

    def test_count(self):
        self.assertEqual(2, User.count())

    def test_get_by(self):
        self.assertEqual(self.john, User.get_by(userid='john'))
        self.assertIsNone(User.get_by(firstname='blabla'))

    def test_get_one(self):
        self.assertEqual(self.hugo, User.get_one(userid='hugo'))
        with self.assertRaises(NoResultFound):
            User.get_one(userid='asd')

    def test_get(self):
        self.assertEqual(self.john, User.get('john'))
        self.assertIsNone(User.get('asds'))
