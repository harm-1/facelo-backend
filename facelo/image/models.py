# -*- coding: utf-8 -*-
"""Image models."""
import datetime as dt

from facelo.database import Column, Model, SurrogatePK, db, relationship, reference_col

from sqlalchemy.dialects.mysql import TINYINT

class Image(SurrogatePK, Model):

    __tablename__ = 'images'
    image_url = Column(db.String(100), nullable=False)
    created = Column(db.DateTime, nullable=False)
    uploaded = Column(db.DateTime, nullable=False)
    age_in_image = Column(TINYINT(unsigned=True))

    # The image has a many-to-one relationship with the user.
    user_id = reference_col('users', nullable=False)
    user = relationship('User', back_populates='images')

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Image({image_url!r})>'.format(image_url=self.image_url)
