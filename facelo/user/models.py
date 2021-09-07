
# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from facelo.database import Column, Model, SurrogatePK, db, relationship
from facelo.extensions import bcrypt

from sqlalchemy.dialects.mysql import TINYINT

class User(SurrogatePK, Model):

    __tablename__ = 'users'
    email = Column(db.String(100), unique=True, nullable=False)
    password = Column(db.LargeBinary(128))
    birth_day = Column(db.Date, nullable=False)
    gender = Column(TINYINT(unsigned=True))
    sexual_preference = Column(TINYINT(unsigned=True))
    karma = Column(db.Integer)
    token: str = ''

    # The user has a one-to-many relationship with the image.
    images = relationship('Image', back_populates='user', cascade="all, delete-orphan")


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
        return '<User({email!r})>'.format(email=self.email)
