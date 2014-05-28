from opengever.ogds.models import BASE
from sqlalchemy import Column, String, Boolean, Text


class User(BASE):
    """User model
    """

    __tablename__ = 'users'

    userid = Column(String(255), primary_key=True)
    active = Column(Boolean, default=True)
    firstname = Column(String(50))
    lastname = Column(String(50))

    directorate = Column(String(50))
    directorate_abbr = Column(String(10))
    department = Column(String(50))
    department_abbr = Column(String(10))

    email = Column(String(50))
    email2 = Column(String(50))
    url = Column(String(100))
    phone_office = Column(String(30))
    phone_fax = Column(String(30))
    phone_mobile = Column(String(30))

    salutation = Column(String(30))
    description = Column(Text())
    address1 = Column(String(100))
    address2 = Column(String(100))
    zip_code = Column(String(10))
    city = Column(String(100))

    country = Column(String(20))

    import_stamp = Column(String(26))

    def __init__(self, userid, **kwargs):
        self.userid = userid
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return '<User %s>' % self.userid

    def label(self):
        return "%s (%s)" % (self.fullname(), self.userid)

    def fullname(self):
        """return a visual representation of the UserPersona as String.
             - The default is "<lastname> <firstname>"
             - If either one is missing it is: "<lastname>" or "<firstname>"
             - The fallback is "<userid>"
        """
        parts = []
        self.lastname and parts.append(self.lastname)
        self.firstname and parts.append(self.firstname)
        len(parts) == 0 and parts.append(self.userid)

        return ' '.join(parts)
