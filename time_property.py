from . import db_access
from .user import User


# these properties allow overriding the current date which should be used in production system with admin override in db
class TimeProperties(db_access.Model):

    def __init__(self, season: int, game_week: int):
        self.season = season
        self.game_week = game_week

    id = db_access.Column(
        db_access.Integer, primary_key=True
    )  # primary keys are required by SQLAlchemy
    season = db_access.Column(db_access.Integer)
    game_week = db_access.Column(db_access.Integer)


PROPERTY_KEY = 1


def current_time_property() -> TimeProperties:
    return TimeProperties.query.get(PROPERTY_KEY)


def save_time_property(season: int, game_week: int):
    prop = TimeProperties.query.get(PROPERTY_KEY)
    prop.season = season
    prop.game_week = game_week
    db_access.session.commit()
