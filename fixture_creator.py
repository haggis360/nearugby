from datetime import datetime
from flask import json
from flask_sqlalchemy import SQLAlchemy


class FixtureCreator:
    def __init__(self, dbaccess: SQLAlchemy) -> None:
        self.db_access = dbaccess

    def create_fixtures(self):
        print("INITIALSING FIXTURES")
        from .fixture import Fixture

        self.db_access.session.query(Fixture).delete()
        for season in range(2011, 2025):
            self.db_access.session.add_all(self.build_fixtures(season))
            self.db_access.session.commit()

    def build_fixtures(self, season: int):
        with open("data/" + str(season) + ".json") as f:
            from . import Fixture

            fixtures = []
            temp = json.load(f)["results"]
            for tr in temp:
                fixtures.append(
                    Fixture(
                        tr["season"],
                        tr["game_week"],
                        tr["venue"],
                        tr["home"],
                        tr["away"],
                        datetime.fromisoformat(tr["date"]),
                    )
                )
            return fixtures
