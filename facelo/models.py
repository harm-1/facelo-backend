# -*- coding: utf-8 -*-
"""models."""
import datetime as dt
from database import (Column, Model, SurrogatePK, db, relationship,
                      reference_col)

from sqlalchemy.dialects.mysql import TINYINT

class UserQuestion(SurrogatePK, Model):

    __tablename__ = 'user_questions'
    score = Column(db.Float)

    # The userQuestion has a many-to-one relationship with the question.
    question_id = reference_col('questions')
    question = relationship('Question')

    # The userQuestion has a many-to-one relationship with the user.
    user_id = reference_col('users')
    user = relationship('User')

