from . import db_access


class PlayerPrediction(db_access.Model):

    def __init__(self, user_id: int, fixture_id: int, home_score: int, away_score: int):
        self.user_id = user_id
        self.fixture_id = fixture_id
        self.home_score = home_score
        self.away_score = away_score
        self.prediction_outcome = 0
        self.prediction_point_diff = 0

    @classmethod
    def populate(
        cls,
        prediction_id: int,
        user_id: int,
        fixture_id: int,
        home_score: int,
        away_score: int,
    ):
        pred = cls(user_id, fixture_id, home_score, away_score)
        pred.id = prediction_id
        return pred

    id = db_access.Column(
        db_access.Integer, primary_key=True
    )  # primary keys are required by SQLAlchemy
    user_id = db_access.Column(db_access.Integer, db_access.ForeignKey("user.id"))
    fixture_id = db_access.Column(db_access.Integer, db_access.ForeignKey("fixture.id"))
    user_rel = db_access.relationship("User", foreign_keys="[PlayerPrediction.user_id]")
    fixture_rel = db_access.relationship(
        "Fixture", foreign_keys="[PlayerPrediction.fixture_id]"
    )
    home_score = db_access.Column(db_access.String(100))
    away_score = db_access.Column(db_access.Integer)
    prediction_outcome = db_access.Column(db_access.Integer)
    prediction_point_diff = db_access.Column(db_access.Integer)
