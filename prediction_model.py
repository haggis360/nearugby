import logging
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, select, text

from .api_loader import APIResultLoader
from .fixture import Fixture
from .json_loader import JsonResultLoader
from .player_prediction import PlayerPrediction
from . import PRODUCTION_ENVIRONMENT


class PredictionModel:

    def __init__(self, dbaccess: SQLAlchemy) -> None:
        self.db_access = dbaccess
        self.loader = (
            APIResultLoader() if PRODUCTION_ENVIRONMENT else JsonResultLoader()
        )

    def clear_predictions(self):
        # set them all to 0
        PlayerPrediction.query.update(
            {
                PlayerPrediction.prediction_outcome: 0,
                PlayerPrediction.prediction_point_diff: 0,
            }
        )
        self.db_access.session.commit()

    def predictions_for_result(self, result):
        cmd = "select p.id, p.home_score, p.away_score from player_prediction p, fixture f where p.fixture_id=f.id and f.season = :s and f.game_week = :g and f.home_team = :home_team and f.away_team = :away_team"
        rseason = result["season"]
        rgame_week = result["game_week"]
        rhome_team = result["home"]
        raway_team = result["away"]
        predictions = self.db_access.session.execute(
            text(cmd),
            {
                "s": rseason,
                "g": rgame_week,
                "home_team": rhome_team,
                "away_team": raway_team,
            },
        )
        return predictions

    # delete all prediction resultds, then get results for current season to gameweek only - we do not care about previous seasons!!
    # then calc the prediction outcome and point dif
    def calculate_predictions(self):
        logging.basicConfig()
        logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
        self.clear_predictions()
        # stopped working this..but only when its called from the admin date update
        results_to_date = self.loader.get_season_results_to_date()
        for result in results_to_date:
            # get the predictions
            predictions = self.predictions_for_result(result)
            for preddata in predictions:
                pid = preddata[0]
                phome = int(preddata[1])
                paway = int(preddata[2])
                rhome = result["home_score"]
                raway = result["away_score"]
                # work out if the result prediction was correct  - gives true/false want 1 or 0
                prediction_outcome = ((rhome - raway < 0) == (phome - paway < 0)) | 0
                # work out the point difference modulus(home - predhome)+modulus(away-predaway) = pred prediction_point_diff
                prediction_point_diff = abs(rhome - phome) + abs(raway - paway)
                #  set in the pred and commit it or session.execute each statement then commit and close
                cmd = "update player_prediction set prediction_outcome = :outcome, prediction_point_diff = :diff where id =:pid"
                self.db_access.session.execute(
                    text(cmd),
                    {
                        "outcome": prediction_outcome,
                        "diff": prediction_point_diff,
                        "pid": pid,
                    },
                )
        self.db_access.session.commit()
        return

    def predictions_for_season_week(self, season: int, game_week: int, userId: int):
        query_stmnt = select(Fixture).where(
            (Fixture.season == season) & (Fixture.game_week == game_week)
        )
        fixtures = self.db_access.session.scalars(query_stmnt)
        predictions = PlayerPrediction.query.filter(
            and_(
                PlayerPrediction.fixture_rel.has(season=season),
                PlayerPrediction.fixture_rel.has(game_week=game_week),
            )
        )
        all_predictions = []
        for fixture in fixtures:
            # get a prediction from the prediction array by fixture id
            for prediction in predictions:
                if prediction.fixture_id == fixture.id:
                    all_predictions.append(prediction)
                    break
            else:
                player_pred = PlayerPrediction(userId, fixture.id, 0, 0)
                player_pred.fixture_rel = fixture
                all_predictions.append(player_pred)
        return all_predictions

    def save_prediction(self, prediction: PlayerPrediction):
        # insert
        saved_prediction = PlayerPrediction.query.get(prediction.id)
        print("SAVE PREDICTION"+prediction.id)
        print(prediction)
        if not saved_prediction:
            prediction.id = None
            self.db_access.session.add(prediction)
        # or update
        else:
            saved_prediction.home_score = prediction.home_score
            saved_prediction.away_score = prediction.away_score
        self.db_access.session.commit()
