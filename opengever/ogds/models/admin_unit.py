from opengever.ogds.models import BASE
from opengever.ogds.models.org_unit import OrgUnit
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship


class AdminUnit(BASE):

    __tablename__ = 'admin_units'

    unit_id = Column(String(30), primary_key=True)
    title = Column(String(30))
    enabled = Column(Boolean(), default=True)
    ip_address = Column(String(50))
    site_url = Column(String(100))
    public_url = Column(String(100))

    clients = relationship("Client", backref="admin_unit")

    def __init__(self, unit_id, **kwargs):
        self.unit_id = unit_id
        super(AdminUnit, self).__init__(**kwargs)

    def __repr__(self):
        return '<AdminUnit %s>' % self.unit_id

    def id(self):
        return self.unit_id

    def label(self):
        return self.title

    def assigned_users(self):
        users = []
        for org_unit in self.org_units:
            users += org_unit.assigned_users()

        return users

    @property
    def org_units(self):
        return [OrgUnit(client) for client in self.clients]

    @org_units.setter
    def org_units(self, units):
        self.clients = [unit._client for unit in units]
