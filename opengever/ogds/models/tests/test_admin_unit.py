from opengever.ogds.models.admin_unit import AdminUnit
from opengever.ogds.models.client import Client
from opengever.ogds.models.group import Group
from opengever.ogds.models.org_unit import OrgUnit
from opengever.ogds.models.testing import DATABASE_LAYER
from opengever.ogds.models.user import User
import unittest2


class TestAdminUnit(unittest2.TestCase):

    layer = DATABASE_LAYER

    @property
    def session(self):
        return self.layer.session

    def setUp(self):
        super(TestAdminUnit, self).setUp()
        self.john = User('john')
        self.hugo = User('hugo')
        self.session.add(self.john)
        self.session.add(self.hugo)

        self.admin_unit = AdminUnit('canton', title='Canton Unit',
                                    ip_address="127.8.9.78")

        self.session.add(self.admin_unit)

        members = Group('members', users=[self.john, self.hugo])
        self.session.add(members)

        client_a = Client('clienta',
                          title='Client A',
                          public_url='http://localhost',
                          users_group=members,
                          admin_unit_id='canton')

        self.session.add(client_a)
        self.org_unit = OrgUnit(client_a)

    def test_representation_returns_OrgUnit_and_id(self):
        self.assertEquals(
            '<AdminUnit canton>',
            self.admin_unit.__repr__())

    def test_label_returns_unit_title(self):
        self.assertEquals(
            'Canton Unit',
            self.admin_unit.label())

    def test_id_returns_unit_id(self):
        self.assertEquals(
            'canton',
            self.admin_unit.id())
