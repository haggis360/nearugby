from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select

from .api_loader import APIResultLoader
from .fixture import Fixture
from .json_loader import JsonResultLoader
from .team_result import TeamResult
from . import PRODUCTION_ENVIRONMENT


class ResulttModel:

    def __init__(self, dbaccess: SQLAlchemy) -> None:
        self.db_access = dbaccess
        self.loader = (
            APIResultLoader() if PRODUCTION_ENVIRONMENT else JsonResultLoader()
        )

    def results_for_team(self, team, size: int):
        filtered_teams = []
        full_result_history = self.loader.get_historic_results_to_date()
        for tr in full_result_history:
            if tr["home"] == team or tr["away"] == team:
                filtered_teams.append(
                    TeamResult(
                        tr["season"],
                        tr["date"],
                        tr["game_week"],
                        tr["home"],
                        tr["away"],
                        tr["venue"],
                        tr["home_score"],
                        tr["away_score"],
                    )
                )
                filtered_teams.sort(key=lambda result: result.fixture_date)
        return filtered_teams

    def fixtures_for_season_week(self, season: int, game_week: int):
        query_stmnt = (
            select(Fixture)
            .where((Fixture.season == season) & (Fixture.game_week == game_week))
            .order_by(Fixture.date)
        )
        return self.db_access.session.scalars(query_stmnt)

    def results_for_match(self, team, opposition, size: int):
        filtered_results = []
        full_result_history = self.loader.get_historic_results_to_date()
        for tr in full_result_history:
            print(tr)
            if (tr["home"] == team and tr["away"] == opposition) or (
                tr["home"] == opposition and tr["away"] == team
            ):
                filtered_results.append(
                    TeamResult(
                        tr["season"],
                        tr["date"],
                        tr["game_week"],
                        tr["home"],
                        tr["away"],
                        tr["venue"],
                        tr["home_score"],
                        tr["away_score"],
                    )
                )
            filtered_results.sort(key=lambda result: result.fixture_date)
        return filtered_results
