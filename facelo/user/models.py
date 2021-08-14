
# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from facelo.database import Column, Model, SurrogatePK, db
from facelo.extensions import bcrypt


class User(SurrogatePK, Model):

    __tablename__ = 'users'
    email = Column(db.String(100), unique=True, nullable=False)
    password = Column(db.LargeBinary(128))
    token: str = ''

    def __init__(self, **kwargs):
        """Create instance."""
        db.Model.__init__(self, **kwargs)
        self.set_password(kwargs['password'])

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<User({username!r})>'.format(username=self.username)
