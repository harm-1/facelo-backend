# -*- coding: utf-8 -*-
"""Image models."""
import datetime as dt

from facelo.database import (Column, Model, SurrogatePK, db, relationship,
                             reference_col, make_nonupdateable)
from sqlalchemy.dialects.mysql import TINYINT

class Image(SurrogatePK, Model):

    __tablename__ = 'images'
    image_url = Column(db.String(100), nullable=False)
    created = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    date_taken = Column(db.DateTime, default=dt.datetime.utcnow)

    # The image has a many-to-one relationship with the user.
    user_id = reference_col('users', nullable=False)
    user = relationship('User', back_populates='images')


    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Image({image_url!r})>'.format(image_url=self.image_url)


make_nonupdateable(Image.image_url)
make_nonupdateable(Image.created)
