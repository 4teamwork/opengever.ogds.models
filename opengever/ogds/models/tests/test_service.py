from opengever.ogds.models.admin_unit import AdminUnit
from opengever.ogds.models.exceptions import RecordNotFound
from opengever.ogds.models.group import Group
from opengever.ogds.models.org_unit import OrgUnit
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

    def test_fetch_group_by_id(self):
        group = Group('group_a')
        self.session.add(group)

        self.assertEquals(group, self.service.fetch_group("group_a"))

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


class TestOrgUnitCounters(unittest2.TestCase):

    layer = DATABASE_LAYER

    @property
    def session(self):
        return self.layer.session

    def setUp(self):
        super(TestOrgUnitCounters, self).setUp()
        self.service = OGDSService(self.session)

    def test_has_multiple_org_units(self):
        self.session.add(OrgUnit('unitc', title="Unit C"))
        self.session.add(OrgUnit('unita', title="Unit A"))
        self.session.add(OrgUnit('unitb', title="Unit B"))

        self.assertTrue(self.service.has_multiple_org_units())

    def test_falsy_multiple_org_units(self):
        self.session.add(OrgUnit('unitc', title="Unit C"))

        self.assertFalse(self.service.has_multiple_org_units())


class TestServiceOrgUnitMethods(unittest2.TestCase):

    layer = DATABASE_LAYER

    @property
    def session(self):
        return self.layer.session

    def setUp(self):
        super(TestServiceOrgUnitMethods, self).setUp()
        self.service = OGDSService(self.session)

        hugo_boss = User('hugo.boss')
        self.session.add(hugo_boss)

        group_a = Group('group_a', users=[hugo_boss])
        self.session.add(group_a)

        self.admin_unit_1 = AdminUnit('admin_1', title="Admin Unit 1")
        self.admin_unit_2 = AdminUnit('admin_2', title="Admin Unit 2",
                                      enabled=False)
        self.admin_unit_3 = AdminUnit('admin_3', title="Admin Unit 3")

        self.session.add(self.admin_unit_1)
        self.session.add(self.admin_unit_2)
        self.session.add(self.admin_unit_3)

        self.unit_c = OrgUnit('unitc', title="Unit C",
                              users_group=group_a, admin_unit_id="unit_1")
        self.unit_a = OrgUnit('unita', title="Unit A",
                              users_group=group_a, admin_unit_id="unit_1")
        self.unit_b = OrgUnit('unitb', title="Unit B",
                              admin_unit_id="unit_2", enabled=False)
        self.session.add(self.unit_c)
        self.session.add(self.unit_a)
        self.session.add(self.unit_b)

    def test_has_multiple_admin_units(self):
        self.assertTrue(self.service.has_multiple_admin_units())

    def test_has_multiple_admin_units_counts_only_enabled_admin_units(self):
        self.admin_unit_1.enabled = False
        self.admin_unit_2.enabled = False
        self.assertFalse(self.service.has_multiple_admin_units())

    def test_fetch_org_unit_by_unit_id(self):
        unit = self.service.fetch_org_unit('unitc')

        self.assertEquals(self.unit_c, unit)

    def test_fetch_org_unit_returns_none_when_no_org_unit_is_found(self):
        self.assertIsNone(self.service.fetch_org_unit('not-existing-unit'))

    def test_fetch_admin_unit_by_unit_id(self):
        self.assertEquals(self.admin_unit_1,
                          self.service.fetch_admin_unit('admin_1'))

    def test_fetching_disabled_admin_unit_by_unit_id(self):
        self.assertEquals(self.admin_unit_2,
                          self.service.fetch_admin_unit('admin_2'))

    def test_fetch_not_existing_admin_unit_returns_none(self):
        self.assertIsNone(self.service.fetch_admin_unit('admin_xx'))

    def test_assigned_org_units_returns_a_list_of_orgunit(self):
        units = self.service.assigned_org_units('hugo.boss')

        self.assertSequenceEqual([self.unit_a, self.unit_c], units)

    def test_all_org_units_returns_list_of_all_orgunits(self):
        units = self.service.all_org_units()

        self.assertSequenceEqual([self.unit_a, self.unit_c], units)

    def test_all_org_units_includes_disabled_orgunits_when_flag_is_set(self):
        units = self.service.all_org_units(enabled_only=False)

        self.assertSequenceEqual([self.unit_a, self.unit_b, self.unit_c],
                                 units)

    def test_all_admin_units_returns_a_list_of_all_enabled_admin_units(self):
        self.assertSequenceEqual([self.admin_unit_1, self.admin_unit_3],
                                 self.service.all_admin_units())

    def test_all_admin_units_includes_disabled_orgunits_when_flag_is_set(self):
        self.assertSequenceEqual(
            [self.admin_unit_1, self.admin_unit_2, self.admin_unit_3],
            self.service.all_admin_units(enabled_only=False))
