from opengever.ogds.models.exceptions import RecordNotFound
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
        return self.session.query(User).get(userid)

    def all_users(self):
        return self.session.query(User).all()

    def inactive_users(self):
        return self.session.query(User).filter_by(active=False).all()
