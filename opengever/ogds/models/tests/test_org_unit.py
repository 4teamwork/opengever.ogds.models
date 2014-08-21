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

        self.org_unit = OrgUnit('unit',
                                title='Unit A',
                                users_group=members)

        self.session.add(self.org_unit)

    def test_create_org_unit_id_required(self):
        with self.assertRaises(TypeError):
            OrgUnit()

    def test_creatable(self):
        org_units = self.session.query(OrgUnit).all()
        self.assertEquals(len(org_units), 1)

        unit = org_units[0]
        self.assertEquals(unit.unit_id, 'unit')

    def test_repr(self):
        self.assertEquals(str(OrgUnit('a-unit')),
                          '<OrgUnit a-unit>')

    def test_create_sets_attrs(self):
        attrs = {
            'unit_id': 'unit-two',
            'title': 'Unit two',
            'enabled': False,
            }

        c2 = OrgUnit(**attrs)

        for key, value in attrs.items():
            self.assertEquals(getattr(c2, key), value)

    def test_representation_returns_OrgUnit_and_id(self):
        self.assertEquals('<OrgUnit unit>', repr(self.org_unit))

    def test_comparison_on_id(self):
        self.assertEqual(OrgUnit('aa'), OrgUnit('aa'))
        self.assertNotEqual(OrgUnit('aa'), OrgUnit('bb'))
        self.assertNotEqual(OrgUnit('aa'), object())
        self.assertNotEqual(OrgUnit('aa'), None)

    def test_label_returns_unit_title(self):
        self.assertEquals(
            'Unit A',
            self.org_unit.label())

    def test_id_returns_unit_id(self):
        self.assertEquals(
            'unit',
            self.org_unit.id())

    def test_assigned_users_returns_all_users_from_the_units_usersgroup(self):
        self.assertEquals(
            [self.john, self.hugo], self.org_unit.assigned_users())

    def test_inbox_returns_inbox_according_to_the_org_unit(self):
        inbox = self.org_unit.inbox()

        self.assertEquals('inbox:unit', inbox.id())
        self.assertEquals(self.org_unit, inbox._org_unit)

    def test_label_is_not_prefixed_for_lone_org_unit(self):
        org_unit = self.service.fetch_org_unit('unit')
        self.assertEqual(u'a label', org_unit.prefix_label(u'a label'))

    def test_label_is_prefixed_for_multiple_org_unit(self):
        self.session.add(OrgUnit('unit-two'))

        org_unit = self.service.fetch_org_unit('unit')
        self.assertEqual(u'Unit A / a label',
                         org_unit.prefix_label(u'a label'))

    def test_inboxgroup_agency_is_inactive_for_lone_org_unit(self):
        org_unit = self.service.fetch_org_unit('unit')

        self.assertFalse(org_unit.is_inboxgroup_agency_active)

    def test_inboxgroup_agency_is_active_for_multiple_org_units(self):
        self.session.add(OrgUnit('unitb'))

        org_unit = self.service.fetch_org_unit('unit')
        self.assertTrue(org_unit.is_inboxgroup_agency_active)


class TestUnitGroups(unittest2.TestCase):

    layer = DATABASE_LAYER

    @property
    def session(self):
        return self.layer.session

    def setUp(self):
        super(TestUnitGroups, self).setUp()

        self.john = User('john')
        self.hugo = User('hugo')
        self.james = User('james')
        self.session.add(self.john)
        self.session.add(self.hugo)
        self.session.add(self.james)

        inbox = Group('inbox', users=[self.john])
        members = Group('members', users=[self.john, self.hugo])
        self.session.add(inbox)
        self.session.add(members)

        self.unit = OrgUnit('unit', users_group=members, inbox_group=inbox)
        self.session.add(self.unit)

    def test_users_in_members_group(self):

        self.assertEquals([self.john, self.hugo],
                          self.unit.users_group.users)

    def test_users_in_inbox_group(self):
        self.assertEquals([self.john],
                          self.unit.inbox_group.users)

    def test_assigned_users_returns_all_users_from_the_usersgroup(self):
        self.assertEquals([self.john, self.hugo],
                          self.unit.assigned_users())
