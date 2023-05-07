# -*- coding: utf-8 -*-
"""Image models."""
import datetime as dt

from facelo.database import (Column, Model, SurrogatePK, db, reference_col, relationship)
from sqlalchemy.dialects.mysql import TINYINT


class Image(SurrogatePK, Model):

    __tablename__ = "images"
    filename = Column(db.String(100), nullable=False)
    created = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    date_taken = Column(db.DateTime, default=dt.datetime.utcnow)

    # The image has a many-to-one relationship with the user.
    user_id = reference_col("users", nullable=False)
    user = relationship("User", back_populates="images")

    # The image has a one-to-many relationship with the trial.
    trials = relationship("Trial", back_populates="image", cascade="all, delete-orphan")

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<Image({image_url!r})>".format(image_url=self.filename)
