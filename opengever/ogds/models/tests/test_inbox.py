from opengever.ogds.models.group import Group
from opengever.ogds.models.inbox import Inbox
from opengever.ogds.models.org_unit import OrgUnit
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

        org_unit = OrgUnit('org',
                           title='Unit A',
                           users_group=members,
                           inbox_group=inbox_members)
        self.session.add(org_unit)

        self.inbox = Inbox(org_unit)

    def test_id_is_refixed_with_inbox_and_colon(self):
        self.assertEquals('inbox:org', self.inbox.id())

    def test_representation(self):
        self.assertEquals('<Inbox inbox:org>', repr(self.inbox))

    def test_assigned_users_list_users_from_org_units_inbox_group(self):
        self.assertEquals([self.john, self.peter],
                          self.inbox.assigned_users())
