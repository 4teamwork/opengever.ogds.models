from sqlalchemy import or_
from sqlalchemy.orm import Query
from sqlalchemy.orm.util import _entity_descriptor


class BaseQuery(Query):

    searchable_fields = []

    def _attribute(self, name):
        """ Return keyword expressions extracted from the primary
        entity of the query, or the last entity that was the
        target of a call to `.Query.join`.

        """
        return _entity_descriptor(self._joinpoint_zero(), name)

    def by_searchable_text(self, text_filters=[]):
        """Extends the given `query` with text_filters, a list of text snippets.
        """

        query = self

        if text_filters:
            # extend the text snippets with the default wildcards
            # and then search for every word seperately
            for word in text_filters:
                term = '%%{0}%%'.format(word)
                fields = [self._attribute(f) for f in self.searchable_fields]
                query = query.filter(
                    or_(*[field.like(term) for field in fields]))

        return query
