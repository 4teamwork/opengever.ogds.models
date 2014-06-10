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
        self.peter = User('peter')
        self.session.add(self.john)
        self.session.add(self.hugo)
        self.session.add(self.peter)

        members_a = Group('members', users=[self.john, self.hugo])
        self.session.add(members_a)

        members_b = Group('members', users=[self.peter, self.hugo])
        self.session.add(members_b)

        self.client_a = Client('clienta',
                          title='Client A',
                          public_url='http://localhost',
                          users_group=members_a,
                          admin_unit_id='canton')
        self.session.add(self.client_a)
        self.org_unit_a = OrgUnit(self.client_a)

        self.client_b = Client('clientb',
                          title='Client B',
                          public_url='http://localhost',
                          users_group=members_b,
                          admin_unit_id='canton')
        self.session.add(self.client_b)

        self.admin_unit = AdminUnit('canton', title='Canton Unit',
                                    ip_address="127.8.9.78",
                                    clients=[self.client_a, self.client_b])
        self.session.add(self.admin_unit)

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

    def test_org_units_getter_returns_client_wrapped_as_orgunits(self):
        self.assertEqual(['<OrgUnit clienta>', '<OrgUnit clientb>'],
                         [unit.__repr__() for unit in self.admin_unit.org_units])

    def test_org_unit_setter_updates_client_relations(self):
        self.admin_unit.org_units = [self.org_unit_a]
        self.assertEqual([self.client_a], self.admin_unit.clients)
