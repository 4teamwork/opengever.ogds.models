from opengever.ogds.models.user import User
from opengever.ogds.models.testing import DATABASE_LAYER
import unittest2


class TestUserModel(unittest2.TestCase):

    layer = DATABASE_LAYER

    @property
    def session(self):
        return self.layer.session

    def test_create_userid_required(self):
        with self.assertRaises(TypeError):
            User()

    def test_creatable(self):
        u1 = User('user-one')
        self.session.add(u1)
        self.session.commit()

        users = self.session.query(User).all()
        self.assertEquals(len(users), 1)

        u1 = users[0]
        self.assertEquals(u1.userid, 'user-one')

    def test_create_sets_attrs(self):
        attrs = {
            'userid': 'hugo.boss',
            'active': True,
            'firstname': 'Hugo',
            'lastname': 'Boss',

            'directorate_abbr': 'FD',
            'directorate': 'Finanzdepartement',
            'department_abbr': 'FV',
            'department': 'Finanzverwaltung',

            'email': 'hugo@boss.ch',
            'email2': 'hugo@boss.com',
            'url': 'http://boss.ch',
            'phone_office': '012 345 67 89',
            'phone_fax': '012 345 67 81',
            'phone_mobile': '079 123 45 67',

            'salutation': 'Herr',
            'description': 'Meister Boss',
            'address1': 'Bossstrasse 1',
            'address2': 'Oberes Bosshaus',
            'zip_code': '1234',
            'city': 'Bossingen',

            'country': 'Schweiz',

            'import_stamp': 'stamp',
            }

        u2 = User(**attrs)

        for key, value in attrs.items():
            self.assertEquals(getattr(u2, key), value)
