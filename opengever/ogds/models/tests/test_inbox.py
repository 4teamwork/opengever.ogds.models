from opengever.ogds.models.client import Client
from opengever.ogds.models.group import Group
from opengever.ogds.models.org_unit import OrgUnit
from opengever.ogds.models.inbox import Inbox
from opengever.ogds.models.testing import DATABASE_LAYER
from opengever.ogds.models.user import User
import unittest2


class TestInbox(unittest2.TestCase):

    layer = DATABASE_LAYER

    @property
    def session(self):
        return self.layer.session

    def setUp(self):
        super(TestInbox, self).setUp()
        self.john = User('john')
        self.hugo = User('hugo')
        self.peter = User('peter')
        self.session.add(self.john)
        self.session.add(self.hugo)
        self.session.add(self.peter)

        members = Group('members', users=[self.john, self.hugo, self.peter])
        self.session.add(members)

        inbox_members = Group('members', users=[self.john, self.peter])
        self.session.add(inbox_members)

        client_a = Client('clienta',
                          title='Client A',
                          public_url='http://localhost',
                          users_group=members,
                          inbox_group=inbox_members)

        org_unit = OrgUnit(client_a)

        self.session.add(client_a)

        self.inbox = Inbox(org_unit)

    def test_id_is_clients_id_prefixed_with_inbox_and_point(self):
        self.assertEquals('inbox:clienta', self.inbox.id())

    def test_representation(self):
        self.assertEquals('<Inbox inbox:clienta>', self.inbox.__repr__())

    def test_assigned_users_list_users_from_clients_inbox_group(self):
        self.assertEquals([self.john, self.peter],
                          self.inbox.assigned_users())
