from opengever.ogds.models.client import Client
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
