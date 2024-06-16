"""
model.py
--------
Implements the model for rugby result data by simulating a database.

Note: although this is nice as a simple example, don't do this in a real-world
production setting. Having a global object for application data is asking for
trouble. Instead, use a real database layer, like
https://flask-sqlalchemy.palletsprojects.com/.
"""

from datetime import datetime
import json

from .teamresult import TeamResult
from flask_login import UserMixin
from . import CURRENT_DATE, dbu


class User(UserMixin, dbu.Model):
    id = dbu.Column(dbu.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = dbu.Column(dbu.String(100), unique=True)
    password = dbu.Column(dbu.String(100))
    name = dbu.Column(dbu.String(1000))


class PlayerPrediction(dbu.Model):
    id = dbu.Column(dbu.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    user_id = dbu.Column(dbu.Integer, dbu.ForeignKey('user.id'))
    fixture_id = dbu.Column(dbu.Integer, dbu.ForeignKey('fixture.id'))
    user_rel = dbu.relationship("User", foreign_keys="[PlayerPrediction.user_id]")
    fixture_rel = dbu.relationship("Fixture", foreign_keys="[PlayerPrediction.fixture_id]")
    home_score = dbu.Column(dbu.String(100))
    away_score = dbu.Column(dbu.Integer)
    prediction_outcome = dbu.Column(dbu.Integer)
    prediction_point_diff = dbu.Column(dbu.Integer)


class Fixture(dbu.Model):
    
    def __init__(self, season: int, game_week: int, venue: str, home_team: str, away_team: str, date: datetime):
        self.season = season
        self.game_week = game_week
        self.venue = venue
        self.home_team = home_team
        self.away_team = away_team
        self.dateTime = date
        
    id = dbu.Column(dbu.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    season = dbu.Column(dbu.String(100))
    game_week = dbu.Column(dbu.String(10))
    venue = dbu.Column(dbu.String(100))
    home_team = dbu.Column(dbu.String(100))
    away_team = dbu.Column(dbu.String(100))
    date = dbu.Column(dbu.DateTime())


RESULT = "Result"
COMP_NAME = ["T14", "TOP 14", "TOP14"]#dirty data that we have to provide tolerance for


#get all the api data. this wll be pretty static as its not the rugby season but we can use it to generate future fixtures by mangling data
def load_full_db():
    with open("data/rugby_data_db.json") as f:
        return json.load(f)

def result_date_compare(result):
  return datetime.fromisoformat(result["date"]) < CURRENT_DATE and (result["comp_name"] in COMP_NAME and result["status"] == RESULT)

#for testing we need to simulate different points in the season to see prediction and past date points
def load_db_todate():
    with open("data/rugby_data_db.json") as f:
        temp = json.load(f)
        ress = list(filter(result_date_compare, temp["results"]))
        print("LOADIN")
        return ress
#never do this - our api is read only. we cache tthe results to a file but pretend these dont exist
#def save_db():
#    with open("data/rugby__data_db.json", 'w') as f:
#        return json.dump(db, f)


def results_for_team(team, size: int):
    filtered_teams = []
    for tr in db:
        if tr["home"] == team or tr["away"] == team:
            filtered_teams.append(TeamResult(tr["season"], tr["date"], 
                                            tr["game_week"], tr["home"], 
                                            tr["away"], tr["venue"], 
                                            tr["home_score"], 
                                            tr["away_score"]))
            filtered_teams.sort(key=lambda result: result.fixture_date)
    return filtered_teams


def results_for_match(team, opposition, size: int):
    print("SIZE: ")
    print(team+' '+opposition)
    filtered_results = []
    print(db)
    for tr in db:
        if (tr["home"] == team  and tr["away"] == opposition) or  (tr["home"] == opposition  and tr["away"] == team):
            filtered_results.append(TeamResult(tr["season"], tr["date"], 
                                                tr["game_week"], tr["home"], 
                                                tr["away"], tr["venue"], 
                                                tr["home_score"], 
                                                tr["away_score"]))
        filtered_results.sort(key=lambda result: result.fixture_date)
    return filtered_results

# this should be in the init
def team_names():
    teamnames = []
    for r in db["results"]:
        if r["home"] not in teamnames:  # Check if the team is already in the list
            teamnames.append(r["home"])  # Add the team to the list if it's not there
        if r["away"] not in teamnames:  # Check if the team is already in the list
            teamnames.append(r["away"])  # Add the team to the list if it's not there
    teamnames.sort()
    return teamnames


def latest_team_form(team):
    pass
        

def latest_match_form():
    pass


db = load_db_todate()
