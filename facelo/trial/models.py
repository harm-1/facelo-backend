# -*- coding: utf-8 -*-
"""Image models."""
from facelo.database import (Column, Model, SurrogatePK, db, reference_col,
                             relationship)


class Trial(SurrogatePK, Model):
    """
    When the user uploads an image, they want to know if that
    image does well for some question.
    e.g. "Who looks better in this image"
    So when a user wants to test a image for some question.
    This Trial object is created.
    """

    __tablename__ = "trials"

    score = Column(db.Float)
    judge_age_min = Column(db.Integer)
    judge_age_max = Column(db.Integer)

    image_id = reference_col("images", nullable=False)
    image = relationship("Image", back_populates="trials")

    question_id = reference_col("questions", nullable=True)
    question = relationship("Question", back_populates="trials")

    challenges = relationship(
        "Challenge",
        primaryjoin="or_(Trial.id==Challenge.winner_id,"
        "Trial.id==Challenge.loser_id)",
    )

    def __lt__(self, other):
        return self.id < other.id
