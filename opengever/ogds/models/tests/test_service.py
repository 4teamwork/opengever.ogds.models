from opengever.ogds.models.exceptions import RecordNotFound
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
