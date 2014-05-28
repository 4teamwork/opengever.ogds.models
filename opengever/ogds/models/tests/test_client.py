from opengever.ogds.models.client import Client
from opengever.ogds.models.group import Group
from opengever.ogds.models.testing import DATABASE_LAYER
from opengever.ogds.models.user import User
import unittest2


class TestClientModel(unittest2.TestCase):

    layer = DATABASE_LAYER

    @property
    def session(self):
        return self.layer.session

    def test_create_clientid_required(self):
        with self.assertRaises(TypeError):
            Client()

    def test_creatable(self):
        c1 = Client('client-one')
        self.session.add(c1)
        self.layer.commit()

        clients = self.session.query(Client).all()
        self.assertEquals(len(clients), 1)

        c1 = clients[0]
        self.assertEquals(c1.client_id, 'client-one')

    def test_repr(self):
        self.assertEquals(str(Client('a-client')),
                          '<Client a-client>')

    def test_create_sets_attrs(self):
        attrs = {
            'client_id': 'client-two',
            'title': 'Client two',
            'enabled': False,
            'ip_address': '127.0.0.5',
            'site_url': 'http://localhost/c2',
            'public_url': 'http://localhost/client2',
            }

        c2 = Client(**attrs)

        for key, value in attrs.items():
            self.assertEquals(getattr(c2, key), value)


class TestClientGroups(unittest2.TestCase):

    layer = DATABASE_LAYER

    @property
    def session(self):
        return self.layer.session

    def setUp(self):
        super(TestClientGroups, self).setUp()

        self.john = User('john')
        self.hugo = User('hugo')
        self.james = User('james')
        self.session.add(self.john)
        self.session.add(self.hugo)
        self.session.add(self.james)

        inbox = Group('inbox', users=[self.john])
        members = Group('members', users=[self.john, self.hugo])
        self.session.add(inbox)
        self.session.add(members)

        self.client = Client('client', users_group=members, inbox_group=inbox)
        self.session.add(self.client)

    def test_users_in_members_group(self):

        self.assertEquals([self.john, self.hugo],
                          self.client.users_group.users)

    def test_users_in_inbox_group(self):
        self.assertEquals([self.john],
                          self.client.inbox_group.users)

    def test_assigned_users_returns_all_users_from_the_usersgroup(self):
        self.assertEquals([self.john, self.hugo],
                          self.client.assigned_users())
