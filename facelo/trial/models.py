# -*- coding: utf-8 -*-
"""Image models."""
from facelo.database import (Column, Model, SurrogatePK, db, relationship,
                             reference_col)

class Trial(SurrogatePK, Model):

    __tablename__ = 'trials'
    score = Column(db.Float)
    judge_age_min = Column(db.Integer)
    judge_age_max = Column(db.Integer)


    # The trial has a many-to-one relationship with the image.
    image_id = reference_col('images', nullable=False)
    image = relationship('Image', back_populates='trials')

    # The trial has a many-to-one relationship with the question.
    question_id = reference_col('questions', nullable=True)
    question = relationship('Question', back_populates='trials')

    # def __repr__(self):
    #     """Represent instance as a unique string."""
    #     return '<Trial({image_url!r})>'.format(image_url=self.image_url)

