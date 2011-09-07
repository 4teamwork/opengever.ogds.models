from opengever.ogds.models import BASE
from plone.testing import Layer
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class DatabaseLayer(Layer):

    def testSetUp(self):
        self.disconnect()
        self.get_connection()

    def testTearDown(self):
        self.disconnect()

    def get_connection(self):
        if '_engine' not in dir(self) or not self._engine:
            self._engine = create_engine('sqlite://')

            BASE.metadata.bind = self._engine
            BASE.metadata.create_all()

        return self._engine

    def disconnect(self):
        self.close_session()
        self._engine = None

    @property
    def session(self):
        if '_session' not in dir(self) or not self._session:
            self._session = scoped_session(sessionmaker(
                    bind=self.get_connection()))

        return self._session

    def close_session(self):
        if '_session' not in dir(self) or not self._session:
            return False

        else:
            self.session.close()
            return True

    def commit(self):
        self.session.commit()
        self.close_session()


DATABASE_LAYER = DatabaseLayer()
