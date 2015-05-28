from opengever.ogds.models import BASE
from opengever.ogds.models import UNIT_ID_LENGTH
from opengever.ogds.models import UNIT_TITLE_LENGTH
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import relationship


class AdminUnit(BASE):

    __tablename__ = 'admin_units'

    unit_id = Column(String(UNIT_ID_LENGTH), primary_key=True)
    title = Column(String(UNIT_TITLE_LENGTH))
    enabled = Column(Boolean(), default=True)
    ip_address = Column(String(50), nullable=False)
    site_url = Column(String(100), nullable=False)
    public_url = Column(String(100), nullable=False)
    abbreviation = Column(String(50), nullable=False)

    org_units = relationship("OrgUnit", backref="admin_unit")

    def __init__(self, unit_id, **kwargs):
        self.unit_id = unit_id
        super(AdminUnit, self).__init__(**kwargs)

    def __repr__(self):
        return '<AdminUnit %s>' % self.unit_id

    def __eq__(self, other):
        if isinstance(other, AdminUnit):
            return self.id() == other.id()
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    def id(self):
        return self.unit_id

    def label(self):
        return self.title or u''

    def assigned_users(self):
        users = set()
        for org_unit in self.org_units:
            users.update(org_unit.assigned_users())
        return users

    def prefix_label(self, label):
        return u'{0} / {1}'.format(self.label(), label)
