from flask import Blueprint, render_template, abort, request, redirect, url_for
from flask_login import login_required, current_user
from .player_prediction import PlayerPrediction
from .prediction_model import PredictionModel
from .player_model import PlayerModel
from .model import get_player
from .result_model import ResulttModel
from . import db_access
from .time_property import current_time_property, save_time_property
from .team_dict import TeamData


fantleague = Blueprint("fantleague", __name__)
team_image_dict = TeamData()
player_model = PlayerModel(db_access)
prediction_model = PredictionModel(db_access)
result_model = ResulttModel(db_access)


@fantleague.route("/")
def welcome():
    return render_template("welcome.html")


@fantleague.route("/profile", defaults={"player_id": None}, methods=["GET"])
@fantleague.route("/profile/<player_id>")
@login_required
def profile(player_id):
    time_property = current_time_property()
    if player_id is None:
        player = current_user
    else:
        player = get_player(player_id)
    return render_template(
        "profile.html",
        user=current_user,
        time_prop=time_property,
        player=player,
        player_history_func=player_model.player_history,
    )


@fantleague.route("/profile", methods=["POST"])
def admin_view():
    print("POST")
    if current_user.role == "admin":
        print("ADMIN")
        # save the current season and game week reset all predictions recalculate all results upto that date
        save_time_property(request.form["season"], request.form["game_week"])
        #  whenever this is done teh fullresult history must be reloaded and the db todate then recalc predictions
        #  model.db = get_season_results_to_date() called in calculation not needed
        prediction_model.calculate_predictions()
        # return render_template('profile.html', user=current_user, message="UPDATED DATE AND RECALCULATING PREDICTIONS")
        return redirect(url_for("fantleague.profile"))
    else:
        return redirect(url_for("fantleague.profile"))


@fantleague.route("/leagueTable")
def league_table_view():
    timeproperty = current_time_property()
    player_history = player_model.player_results(timeproperty.season)
    return render_template(
        "league_table.html",
        player_results=player_history,
        calc_time=timeproperty,
        player_history_func=player_model.player_history,
    )


@fantleague.route("/match_form/<team>/<opposition>")
def match_view(team, opposition):
    try:
        match_results = result_model.results_for_match(team, opposition, 10)
        return render_template(
            "match_form.html", results=match_results, team=team, opposition=opposition
        )
    except IndexError:
        abort(404)


@fantleague.route("/team_form/<team>")
def team_view(team):
    try:
        team_results = result_model.results_for_team(team, 10)
        return render_template(
            "team_form.html",
            results=team_results,
            team=team,
            team_image_func=team_image_dict.image_for_team,
        )
    except IndexError:
        abort(404)


@fantleague.route("/fixtures/<season>/<game_week>")
def fixture_view(season, game_week):
    try:
        fixtures = result_model.fixtures_for_season_week(season, game_week)
        return render_template(
            "fixtures.html", fixtures=fixtures, season=season, game_week=game_week
        )
    except IndexError:
        abort(404)


@fantleague.route(
    "/add_prediction", defaults={"season": None, "game_week": None}, methods=["GET"]
)
@fantleague.route(
    "/add_prediction/<int:season>/<int:game_week>", methods=["GET", "POST"]
)
@login_required
def add_prediction(season, game_week):
    try:
        if request.method == "POST":
            # form has been submitted, process data FOR EACH.........
            prediction = PlayerPrediction.populate(
                request.form["prediction_id"],
                current_user.id,
                request.form["fixture_id"],
                request.form["home_score"],
                request.form["away_score"],
            )
            # save and redirect
            prediction_model.save_prediction(prediction)
            return redirect(
                url_for("fantleague.add_prediction", season=season, game_week=game_week)
            )
        else:
            # get the list of fixtures and the list of predictions from model for the season and week and send to template
            time_prop = current_time_property()
            if season is None:
                season = time_prop.season
                game_week = time_prop.game_week
            predictions = prediction_model.predictions_for_season_week(
                season, game_week, current_user.id
            )
            readonly = int(season) < time_prop.season or (
                int(season) == time_prop.season
                and int(game_week) <= time_prop.game_week
            )
            pending = (
                int(season) == time_prop.season
                and int(game_week) == time_prop.game_week
            )
            return render_template(
                "add_prediction.html",
                predictions=predictions,
                season=season,
                game_week=game_week,
                ro=readonly,
                pending=pending,
                team_image_func=team_image_dict.image_for_team,
            )
    except IndexError:
        abort(404)
