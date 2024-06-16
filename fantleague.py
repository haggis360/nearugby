from flask import (Blueprint, render_template, abort, jsonify, request,
                   redirect, url_for)
from flask_login import login_required, current_user
from .model import db, results_for_team, results_for_match


fantleague = Blueprint('fantleague', __name__)


@fantleague.route("/")
def welcome():
    return render_template(
        "welcome.html",
        cards=db
    )


@fantleague.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@fantleague.route('/match_form/<team>/<opposition>')
def match_view(team, opposition):
    try:
        match_results = results_for_match(team, opposition, 0)
        print(match_results)
        return render_template("match_form.html",
                               results=match_results,
                               team=team,
                               opposition=opposition)
    except IndexError:
        abort(404)


@fantleague.route('/team_form/<team>')
def team_view(team):
    try:
        team_results = results_for_team(team, 10)
        return render_template("team_form.html",
                               results=team_results,
                               team=team,
                               index=1,
                               max_index=3)
    except IndexError:
        abort(404)


@fantleague.route('/add_prediction/<season>/<game_week>', methods=["GET", "POST"])
@login_required
def add_prediction(season, game_week):
    if request.method == "POST":
        # form has been submitted, process data
        prediction = {"user_id": current_user.id,
                "fixture_id": request.form['fixture_id'],
                "home_score":  request.form['home_score'],
                "away_score": request.form['away_score']}
        #save and redirect
     #   save_prediction(prediction) 
        return redirect(url_for('add_prediction', season, game_week))
    else:
#        get the list of fixtures and the list of predictions from model for the season and week and send to template
#        return render_template("add_prediction.html", fixtures=fixtures, predictions=predictions)
        pass

@fantleague.route('/remove_card/<int:index>', methods=["GET", "POST"])
def remove_card(index):
    try:
        if request.method == "POST":
            del db[index]
            save_db()
            return redirect(url_for('fantleague.welcome'))
        else:
            return render_template("remove_card.html", card=db[index])
    except IndexError:
        abort(404)


@fantleague.route("/api/card/")
def api_card_list():
    return jsonify(db)


@fantleague.route("/api/card/<int:index>")
def api_card_detail(index):
    try:
        return db[index]
    except IndexError:
        abort(404)
