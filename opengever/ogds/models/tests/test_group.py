from opengever.ogds.models.group import Group
from opengever.ogds.models.testing import DATABASE_LAYER
from opengever.ogds.models.user import User
import unittest2


class TestGroupModel(unittest2.TestCase):

    layer = DATABASE_LAYER

    @property
    def session(self):
        return self.layer.session

    def test_create_groupid_required(self):
        with self.assertRaises(TypeError):
            Group()

    def test_creatable(self):
        g1 = Group('group-one')
        self.session.add(g1)
        self.layer.commit()

        groups = self.session.query(Group).all()
        self.assertEquals(len(groups), 1)

        g1 = groups[0]
        self.assertEquals(g1.groupid, 'group-one')

    def test_create_sets_attrs(self):
        attrs = {
            'groupid': 'admins',
            'title': 'Administrators',
            }

        g2 = Group(**attrs)

        for key, value in attrs.items():
            self.assertEquals(getattr(g2, key), value)

    def test_users_in_group(self):
        self.session.add(User('john.doe'))
        self.session.add(Group('users'))
        self.layer.commit()

        # HINT: after committing, re-fetch the objects since the old ones
        # are now bound to a closed session..
        # we use getter-methods for generalization
        def get_john():
            john = self.session.query(User).filter_by(userid='john.doe').one()
            self.assertIsNotNone(john)
            return john

        def get_users():
            users = self.session.query(Group).filter_by(groupid='users').one()
            self.assertIsNotNone(users)
            return users

        # add john to users
        john = get_john()
        users = get_users()

        self.assertNotIn(john, users.users)
        users.users.append(john)
        self.assertIn(john, users.users)
        self.layer.commit()

        john = get_john()
        users = get_users()
        self.assertIn(john, users.users)

        # remove john from users
        users.users.remove(john)
        self.assertNotIn(john, users.users)
        self.layer.commit()

        john = get_john()
        users = get_users()
        self.assertNotIn(john, users.users)
