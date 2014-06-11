from opengever.ogds.models.admin_unit import AdminUnit
from opengever.ogds.models.client import Client
from opengever.ogds.models.exceptions import RecordNotFound
from opengever.ogds.models.group import Group
from opengever.ogds.models.org_unit import LoneOrgUnit
from opengever.ogds.models.org_unit import OrgUnit
from opengever.ogds.models.user import User


class OGDSService(object):

    def __init__(self, session):
        self.session = session

    def find_user(self, userid):
        """returns a User by its userid. When no User is found, this method raises.
           a ValueError.
           See #fetch_user for similar behavior.
        """
        user = self.fetch_user(userid)
        if not user:
            raise RecordNotFound(User, userid)
        return user

    def fetch_user(self, userid):
        """returns a User by it's userid. None is returned when no user is found.
           See #find_user for similar behavior.
        """
        return self._query_user().get(userid)

    def all_users(self):
        return self._query_user().all()

    def inactive_users(self):
        return self._query_user().filter_by(active=False).all()

    def fetch_client(self, client_id):
        """returns a Client by it's client_id. None is returned when no client
        is found. """

        return self._query_client().get(client_id)

    def all_clients(self, enabled_only=True):
        query = self._query_client()
        if enabled_only:
            query = query.filter_by(enabled=True)

        return query.all()

    def assigned_clients(self, userid):
        query = self._query_client().join(Client.users_group)
        query = query.join(Group.users).filter(User.userid == userid)
        return query.all()

    def fetch_org_unit(self, unit_id):
        return self._wrap_client(self.fetch_client(unit_id))

    def all_org_units(self, enabled_only=True):
        clients = self.all_clients(enabled_only=enabled_only)
        return [self._wrap_client(client) for client in clients]

    def assigned_org_units(self, userid):
        return [self._wrap_client(client) for client in
                self.assigned_clients(userid)]

    def _wrap_client(self, client):
        if not client:
            return None
        if self.has_multiple_org_units():
            return OrgUnit(client)
        else:
            return LoneOrgUnit(client)

    def fetch_admin_unit(self, unit_id):
        return self._query_admin_units(enabled_only=False).get(unit_id)

    def all_admin_units(self, enabled_only=True):
        query = self._query_admin_units(enabled_only)
        return query.all()

    def has_multiple_admin_units(self, enabled_only=True):
        query = self._query_admin_units(enabled_only)
        return query.count() > 1

    def has_multiple_org_units(self):
        return self._query_client().count() > 1

    def _query_admin_units(self, enabled_only=True):
        query = self.session.query(AdminUnit)
        if enabled_only:
            query = query.filter_by(enabled=enabled_only)
        return query

    def _query_client(self):
        return self.session.query(Client).order_by(Client.title)

    def _query_user(self):
        return self.session.query(User)