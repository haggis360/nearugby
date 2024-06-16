# init.py
import json
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


# init SQLAlchemy so we can use it later in our models
dbu = SQLAlchemy()
with open("current_properties.txt") as f:
    props = json.load(f) 
    CURRENT_SEASON = props["current_season"]
    CURRENT_DATE = datetime.fromisoformat(props["current_date"])
    CURRENT_GAME_WEEK = props["current_game_week"]
    INITIALISE_FIXTURES = props["initialise_fixtures"]=="true" # default to false if not set or cant be read!!

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    dbu.init_app(app)
    with app.app_context():
        from . import model  # load models first
        from .model import User, PlayerPrediction, Fixture
        dbu.create_all()
        if INITIALISE_FIXTURES:
            dbu.session.add_all(build_fixtures())
            dbu.session.commit()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .fantleague import fantleague as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


def build_fixtures():
    with open("data/rugby_data_db.json") as f:
        from .model import Fixture
        fixtures = []
        temp = json.load(f)["results"]
        for tr in temp:
            fixtures.append(Fixture(tr["season"], tr["game_week"], 
                                    tr["venue"], tr["home"], 
                                    tr["away"], datetime.fromisoformat(tr["date"])))
        return fixtures

#def calculate_predictions():
    #for each prediction has the data passed?
    #compare it to the result and record the player 
#    with open("data/rugby_data_db.json") as f:
 #       temp = json.load(f)["results"]
  #      fixtures = list(filter(lambda result: (result<CURRENT_DATE), temp)) 
   #     return fixtures
