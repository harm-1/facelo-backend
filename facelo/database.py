# -*- coding: utf-8 -*-
"""Database module, including the SQLAlchemy database object and DB-related utilities."""
from sqlalchemy import event
from sqlalchemy.orm import relationship
from sqlalchemy.util.langhelpers import symbol

from .compat import basestring
from .extensions import db

# Alias common SQLAlchemy names
Column = db.Column
relationship = relationship
Model = db.Model

# From Mike Bayer's "Building the app" talk
# https://speakerdeck.com/zzzeek/building-the-app
class SurrogatePK(object):
    """A mixin that adds a surrogate integer 'primary key' column named ``id`` \
        to any declarative-mapped class.
    """

    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        if any(
            (
                isinstance(record_id, basestring) and record_id.isdigit(),
                isinstance(record_id, (int, float)),
            ),
        ):
            return cls.query.get(int(record_id))


def reference_col(tablename, nullable=False, pk_name="id", **kwargs):
    """Column that adds primary key foreign key reference.
    Usage: ::
        category_id = reference_col('category')
        category = relationship('Category', backref='categories')
    """
    return db.Column(
        db.ForeignKey("{0}.{1}".format(tablename, pk_name)), nullable=nullable, **kwargs
    )


from sqlalchemy import event
from sqlalchemy.util.langhelpers import symbol


class NonUpdateableColumnError(AttributeError):
    def __init__(self, cls, column, old_value, new_value, message=None):
        self.cls = cls
        self.column = column
        self.old_value = old_value
        self.new_value = new_value

        if message is None:
            self.message = "Cannot update column {} on model {} from {} to {}: column is non-updateable.".format(
                column, cls, old_value, new_value
            )


def make_nonupdateable(col):
    @event.listens_for(col, "set")
    def unupdateable_column_set_listener(target, value, old_value, initiator):
        if (
            old_value != symbol("NEVER_SET")
            and old_value != symbol("NO_VALUE")
            and old_value != value
        ):
            raise NonUpdateableColumnError(
                col.class_.__name__, col.name, old_value, value
            )
