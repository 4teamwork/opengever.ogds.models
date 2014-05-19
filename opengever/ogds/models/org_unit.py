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

    def assigned_users(self):
        return self._client.assigned_users()
