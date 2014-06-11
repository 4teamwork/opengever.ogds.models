from opengever.ogds.models.inbox import Inbox


class OrgUnit(object):

    def __init__(self, client):
        self._client = client

    def __repr__(self):
        return '<OrgUnit %s>' % self.id()

    def id(self):
        return self._client.client_id

    def label(self):
        return self._client.title

    def public_url(self):
        return self._client.public_url

    def inbox_group(self):
        return self._client.inbox_group

    def assigned_users(self):
        return self._client.assigned_users()

    def users_group(self):
        return self._client.users_group

    def assign_to_admin_unit(self, admin_unit):
        admin_unit.org_units.append(self._client)

    def inbox(self):
        return Inbox(self)

    def prefix_label(self, label):
        return u'{0} / {1}'.format(self.label(), label)


class LoneOrgUnit(OrgUnit):
    """Handles special cases when only one OrgUnit is available in the whole
    system.

    """
    def prefix_label(self, label):
        return label
