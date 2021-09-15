# -*- coding: utf-8 -*-
"""Image models."""
from facelo.database import (Column, Model, SurrogatePK, db, relationship,
                             reference_col)

class Question(SurrogatePK, Model):

    __tablename__ = 'questions'

    question = Column(db.String(200), unique=True, nullable=False)

    # The question has an one-to-many relation with the trial
    trials = relationship('Trial', back_populates='question')

    # The question has an one-to-many relation with the challenge
    challenges = relationship('Challenge', back_populates='question')

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Question({question!r})>'.format(question=self.question)
