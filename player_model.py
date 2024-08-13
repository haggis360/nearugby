import logging
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from .player_result import PlayerResult
from .time_property import current_time_property


class PlayerModel:

    def __init__(self, dbaccess: SQLAlchemy) -> None:
        self.db_access = dbaccess

    def player_results(self, season: int):
        cmd = "select u.name, p.user_id, sum(p.prediction_outcome) as outcome, sum(p.prediction_point_diff) as diff from player_prediction p, fixture f, user u where p.user_id=u.id and p.fixture_id=f.id and f.season=:seas group by p.user_id order by outcome desc"
        dbplayer_results = self.db_access.session.execute(text(cmd), {"seas": season})
        player_res = []
        for dbplayer_result in dbplayer_results:
            player_res.append(
                PlayerResult(
                    dbplayer_result[1],
                    dbplayer_result[0],
                    dbplayer_result[2],
                    dbplayer_result[3],
                )
            )
        return player_res

    def player_history(self, user_id: int):
        logging.basicConfig()
        logging.getLogger("sqlalchemy.session").setLevel(logging.DEBUG)
        time = current_time_property()
        cmd = "select u.name, p.user_id, p.prediction_outcome from player_prediction p, user u, fixture f where u.id =:user_id and p.user_id = u.id and p.fixture_id = f.id and ((f.season = :season and f.game_week < :gweek) or f.season < :season) order by f.date desc limit 5"
        dbplayer_results = self.db_access.session.execute(
            text(cmd),
            {"user_id": user_id, "season": time.season, "gweek": time.game_week},
        )
        player_results = []
        for dbplayer_result in dbplayer_results:
            player_results.append(
                PlayerResult(
                    dbplayer_result[1], dbplayer_result[0], dbplayer_result[2], 0
                )
            )
        return player_results
