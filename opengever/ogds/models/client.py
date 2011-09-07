from opengever.ogds.models import BASE
from opengever.ogds.models.group import Group
from sqlalchemy import Column, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Client(BASE):
    """Client model
    """

    __tablename__ = 'clients'

    client_id = Column(String(30), primary_key=True)
    title = Column(String(30))
    enabled = Column(Boolean(), default=True)
    ip_address = Column(String(50))
    site_url = Column(String(100))
    public_url = Column(String(100))

    # ehemals group
    users_group_id = Column(String(30), ForeignKey('groups.groupid'))
    users_group = relationship(
        "Group",
        backref='client_group',
        primaryjoin=users_group_id == Group.groupid)

    inbox_group_id = Column(String(30), ForeignKey('groups.groupid'))
    inbox_group = relationship(
        "Group",
        backref='inbox_group',
        primaryjoin=inbox_group_id == Group.groupid)

    def __init__(self, client_id, **kwargs):
        self.client_id = client_id
        for key, value in kwargs.items():
            # provoke a AttributeError
            getattr(self, key)
            setattr(self, key, value)

    def __repr__(self):
        return '<Client %s>' % self.client_id
