from opengever.ogds.models.client import Client
from opengever.ogds.models.exceptions import RecordNotFound
from opengever.ogds.models.group import Group
from opengever.ogds.models.service import OGDSService
from opengever.ogds.models.testing import DATABASE_LAYER
from opengever.ogds.models.user import User
import unittest2


class TestOGDSService(unittest2.TestCase):

    layer = DATABASE_LAYER

    @property
    def session(self):
        return self.layer.session

    def setUp(self):
        super(TestOGDSService, self).setUp()
        self.service = OGDSService(self.session)

    def test_fetch_user_by_id(self):
        jane = User("jane")
        self.session.add(jane)

        self.assertEquals(jane, self.service.fetch_user("jane"))

    def test_fetch_user_returns_none_when_no_user_found(self):
        self.assertEquals(None, self.service.fetch_user("jane"))

    def test_find_user_user_by_id(self):
        jane = User("jane")
        self.session.add(jane)
        self.assertEquals(jane, self.service.find_user("jane"))

    def test_find_user_raise_when_no_user_found(self):
        with self.assertRaises(RecordNotFound) as cm:
            self.service.find_user("jane")

        self.assertEquals("no User found for jane",
                          str(cm.exception))

    def test_all_users_returns_a_list_of_every_user(self):
        jane = User("jane")
        self.session.add(jane)
        peter = User("peter")
        self.session.add(peter)

        self.assertEquals([jane, peter], self.service.all_users())

    def test_all_users_returns_empty_list_when_no_user_exists(self):
        self.assertEquals([], self.service.all_users())

    def test_inactive_users_filters_by_active_false(self):
        jane = User("jane", active=False)
        self.session.add(jane)
        peter = User("peter", active=True)
        self.session.add(peter)

        self.assertEquals([jane], self.service.inactive_users())


class TestServiceClientMethods(unittest2.TestCase):

    layer = DATABASE_LAYER

    @property
    def session(self):
        return self.layer.session

    def setUp(self):
        super(TestServiceClientMethods, self).setUp()
        self.service = OGDSService(self.session)

        hugo_boss = User('hugo.boss')
        self.session.add(hugo_boss)

        group_a = Group('group_a', users=[hugo_boss])
        self.session.add(group_a)

        self.client_a = Client('clienta', title="Client A", users_group=group_a)
        self.client_b = Client('clientb', title="Client B", enabled=False)
        self.client_c = Client('clientc', title="Client C", users_group=group_a)
        self.session.add(self.client_a)
        self.session.add(self.client_b)
        self.session.add(self.client_c)

    def test_fetch_client_by_client_id(self):
        self.assertEquals(self.client_c,
                          self.service.fetch_client('clientc'))

    def test_fetch_client_returns_none_when_no_client_found(self):
        self.assertEquals(None,
                          self.service.fetch_client('not-existing-client'))
    def test_assigned_clients_returns_a_list_of_all_clients_which_the_user_group_contains_the_given_user(self):
        self.assertEquals(
            [self.client_a, self.client_c],
            self.service.assigned_clients('hugo.boss'))

    def test_assigned_org_units_returns_a_list_all_assigned_clients_wrapped_as_orgunit(self):

        units = self.service.assigned_org_units('hugo.boss')

        self.assertEquals(
            [self.client_a, self.client_c],
            [u._client for u in units])

    def test_all_clients_returns_list_of_all_enabled_clients_by_default(self):
        self.assertEquals(
            [self.client_a, self.client_c],
            self.service.all_clients())

    def test_all_clients_includes_disabled_clients_when_disable_enabled_flag(self):
        self.assertEquals(
            [self.client_a, self.client_c, self.client_b],
            self.service.all_clients(enabled_only=False))

