# -*- coding: utf-8 -*-
"""Challenge models."""
import datetime as dt

from flask_jwt_extended import get_current_user
from sqlalchemy.dialects.mysql import TINYINT

from facelo.database import (Column, Model, SurrogatePK, db, reference_col,
                             relationship)


# TODO add check that winner and loser cant be the same trial
class Challenge(SurrogatePK, Model):

    __tablename__ = "challenges"
    judge_age = Column(db.Integer)
    date = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    type = Column(TINYINT(unsigned=True))
    winner_has_revealed = Column(db.Boolean, default=False)
    loser_has_revealed = Column(db.Boolean, default=False)
    completed = Column(db.Boolean, default=False)

    # The challenge has a many-to-one relationship with the question.
    question_id = reference_col("questions")
    question = relationship("Question", back_populates="challenges")

    # The challenge has a many-to-one relationship with the judge.
    # TODO Dit wordt later een andere tabel, maar ik laat het nu zo
    judge_id = reference_col("users", nullable=True)
    judge = relationship("User", back_populates="judged_challenges")

    # The challenge has a many-to-one relationship with the winning trial.
    winner_id = reference_col("trials", nullable=True)
    winner = relationship("Trial", back_populates="challenges", foreign_keys=winner_id)

    # The challenge has a many-to-one relationship with the losing trial.
    loser_id = reference_col("trials", nullable=True)
    loser = relationship("Trial", back_populates="challenges", foreign_keys=loser_id)

    def complete(self, results):
        assert self.judge == get_current_user()
        assert results["winner_id"] in [self.winner_id, self.loser_id]
        assert results["loser_id"] in [self.winner_id, self.loser_id]
        self.winner_id = results["winner_id"]
        self.loser_id = results["loser_id"]
        self.completed = True
