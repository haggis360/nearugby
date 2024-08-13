import datetime

from . import db_access


class Fixture(db_access.Model):

    def __init__(
        self,
        season: int,
        game_week: int,
        venue: str,
        home_team: str,
        away_team: str,
        date: datetime,
    ):
        self.season = season
        self.game_week = game_week
        self.venue = venue
        self.home_team = home_team
        self.away_team = away_team
        self.date = date

    id = db_access.Column(
        db_access.Integer, primary_key=True
    )  # primary keys are required by SQLAlchemy
    season = db_access.Column(db_access.Integer)
    game_week = db_access.Column(db_access.Integer)
    venue = db_access.Column(db_access.String(100))
    home_team = db_access.Column(db_access.String(100))
    away_team = db_access.Column(db_access.String(100))
    date = db_access.Column(db_access.DateTime())

    def __str__(self):
        return f"Fixture is {self.id} season {self.season} week {self.game_week} home {self.home_team} away {self.away_team}"
