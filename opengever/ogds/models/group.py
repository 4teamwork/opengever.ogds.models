from opengever.ogds.models import BASE
from opengever.ogds.models.user import User
from sqlalchemy import Column, String, Table
from sqlalchemy import ForeignKey
from sqlalchemy.orm import backref, relation


# association table
groups_users = Table(
    'groups_users', BASE.metadata,
    Column('groupid', String(50),
           ForeignKey('groups.groupid'), primary_key=True),
    Column('userid', String(30),
           ForeignKey('users.userid'), primary_key=True),
    )


class Group(BASE):
    """Group model, corresponds to a LDAP group
    """

    __tablename__ = 'groups'

    groupid = Column(String(255), primary_key=True)
    title = Column(String(50))

    users = relation(User, secondary=groups_users,
                     backref=backref('group_users'))

    def __init__(self, groupid, **kwargs):
        self.groupid = groupid

        for key, value in kwargs.items():
            # provoke an AttributeError
            getattr(self, key)
            setattr(self, key, value)

    def __repr__(self):
        return '<Group %s>' % self.groupid
