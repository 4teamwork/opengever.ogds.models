from sqlalchemy.orm import Query
from sqlalchemy.orm.util import _entity_descriptor


class BaseQuery(Query):

    def _attribute(self, name):
        """ Return keyword expressions extracted from the primary
        entity of the query, or the last entity that was the
        target of a call to `.Query.join`.

        """
        return _entity_descriptor(self._joinpoint_zero(), name)
