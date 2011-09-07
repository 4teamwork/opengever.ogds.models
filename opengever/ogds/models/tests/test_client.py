from opengever.ogds.models.client import Client
from opengever.ogds.models.group import Group
from opengever.ogds.models.user import User
from opengever.ogds.models.testing import DATABASE_LAYER
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
        client = Client('client')
        inbox = Group('inbox')
        members = Group('members')
        john = User('john.doe')
        hugo = User('hugo.boss')

        # john and hugo are members
        members.users.append(john)
        members.users.append(hugo)

        # only john is inbox user
        inbox.users.append(john)

        # set the groups on the client
        client.inbox_group = inbox
        client.users_group = members

        self.session.add(client)
        self.layer.commit()

    def _get_user(self, userid):
        return self.session.query(User).filter_by(userid=userid).one()

    def _get_client(self):
        return self.session.query(Client).filter_by(client_id='client').one()

    def test_users_in_members_group(self):
        self.assertIn(self._get_user('john.doe'),
                      self._get_client().users_group.users)

        self.assertIn(self._get_user('hugo.boss'),
                      self._get_client().users_group.users)

    def test_only_john_in_inbox_group(self):
        self.assertIn(self._get_user('john.doe'),
                      self._get_client().inbox_group.users)

        self.assertNotIn(self._get_user('hugo.boss'),
                         self._get_client().inbox_group.users)
