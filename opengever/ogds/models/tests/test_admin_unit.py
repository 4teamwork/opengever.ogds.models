from opengever.ogds.models.admin_unit import AdminUnit
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

        self.org_unit_a = OrgUnit('unita',
                                  title='Unit A',
                                  users_group=members_a,
                                  admin_unit_id='canton')
        self.session.add(self.org_unit_a)

        self.org_unit_b = OrgUnit('unitb',
                                  title='Unit B',
                                  users_group=members_b,
                                  admin_unit_id='canton')
        self.session.add(self.org_unit_b)

        self.admin_unit = AdminUnit('canton', title='Canton Unit',
                                    ip_address="127.8.9.78",
                                    org_units=[
                                        self.org_unit_a,
                                        self.org_unit_b
                                    ])
        self.session.add(self.admin_unit)

    def test_equality(self):
        self.assertEqual(AdminUnit('aa'), AdminUnit('aa'))
        self.assertNotEqual(AdminUnit('aa'), AdminUnit('bb'))
        self.assertNotEqual(AdminUnit('aa'), AdminUnit(123))
        self.assertNotEqual(AdminUnit('aa'), AdminUnit(None))
        self.assertNotEqual(AdminUnit('aa'), object())
        self.assertNotEqual(AdminUnit('aa'), None)

    def test_representation_returns_OrgUnit_and_id(self):
        self.assertEquals('<AdminUnit canton>', repr(self.admin_unit))

    def test_label_returns_unit_title(self):
        self.assertEquals('Canton Unit', self.admin_unit.label())

    def test_label_returns_emtpy_string_when_title_is_none(self):
        self.admin_unit.title = None
        self.assertEquals('', self.admin_unit.label())

    def test_id_returns_unit_id(self):
        self.assertEquals('canton', self.admin_unit.id())

    def test_org_units_getter_returns_correct_orgunits(self):
        self.assertSequenceEqual([self.org_unit_a, self.org_unit_b],
                                 self.admin_unit.org_units)

    def test_assigned_users_return_assigned_users_of_all_orgunits(self):
        self.assertItemsEqual([self.hugo, self.peter, self.john],
                              self.admin_unit.assigned_users())

    def test_prefix_label(self):
        self.assertEqual(u'Canton Unit / foo',
                         self.admin_unit.prefix_label('foo'))
