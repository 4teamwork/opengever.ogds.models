from opengever.ogds.models.admin_unit import AdminUnit
from opengever.ogds.models.client import Client
from opengever.ogds.models.group import Group
from opengever.ogds.models.testing import DATABASE_LAYER
from opengever.ogds.models.user import User
import unittest2


class TestOrgUnit(unittest2.TestCase):

    layer = DATABASE_LAYER

    @property
    def session(self):
        return self.layer.session

    def setUp(self):
        super(TestOrgUnit, self).setUp()
        self.john = User('john')
        self.hugo = User('hugo')
        self.session.add(self.john)
        self.session.add(self.hugo)

        members = Group('members', users=[self.john, self.hugo])
        self.session.add(members)

        client_a = Client('clienta',
                          title='Client A',
                          public_url='http://localhost',
                          users_group=members)

        self.session.add(client_a)
        self.org_unit = AdminUnit(client_a)

    def test_representation_returns_OrgUnit_and_id(self):
        self.assertEquals(
            '<AdminUnit clienta>',
            self.org_unit.__repr__())

    def test_label_returns_client_title(self):
        self.assertEquals(
            'Client A',
            self.org_unit.label())

    def test_id_returns_client_id(self):
        self.assertEquals(
            'clienta',
            self.org_unit.id())

    def test_public_url_returns_clients_public_url(self):
        self.assertEquals(
            'http://localhost',
            self.org_unit.public_url())
