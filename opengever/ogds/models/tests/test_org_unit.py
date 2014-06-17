from opengever.ogds.models.admin_unit import AdminUnit
from opengever.ogds.models.client import Client
from opengever.ogds.models.group import Group
from opengever.ogds.models.org_unit import OrgUnit
from opengever.ogds.models.service import OGDSService
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

        self.service = OGDSService(self.session)

        self.john = User('john')
        self.hugo = User('hugo')
        self.session.add(self.john)
        self.session.add(self.hugo)

        members = Group('members', users=[self.john, self.hugo])
        self.session.add(members)

        self.client_a = Client('clienta',
                          title='Client A',
                          public_url='http://localhost',
                          users_group=members)

        self.session.add(self.client_a)
        self.org_unit = OrgUnit(self.client_a)

    def test_representation_returns_OrgUnit_and_id(self):
        self.assertEquals(
            '<OrgUnit clienta>',
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

    def test_assigned_users_returns_all_users_from_the_clients_usersgroup(self):
        self.assertEquals(
            [self.john, self.hugo], self.org_unit.assigned_users())

    def test_inbox_returns_inbox_according_to_the_org_unit(self):
        inbox = self.org_unit.inbox()

        self.assertEquals('inbox:clienta', inbox.id())
        self.assertEquals(self.org_unit, inbox._org_unit)

    def test_label_is_not_prefixed_for_lone_org_unit(self):
        org_unit = self.service.fetch_org_unit('clienta')
        self.assertEqual(u'a label', org_unit.prefix_label(u'a label'))

    def test_label_is_prefixed_for_multiple_org_unit(self):
        self.session.add(Client('clientb'))

        org_unit = self.service.fetch_org_unit('clienta')
        self.assertEqual(u'Client A / a label',
                         org_unit.prefix_label(u'a label'))

    def test_admin_unit_returns_clients_admin_unit(self):
        admin_unit = AdminUnit('admin_unit_1')
        self.session.add(admin_unit)
        self.client_a.admin_unit_id = admin_unit.id()
        self.session.commit()

        self.assertEqual(admin_unit, self.org_unit.admin_unit)
