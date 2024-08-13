import json
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from .fixture_creator import FixtureCreator


# init SQLAlchemy so we can use it later in our models
db_access = SQLAlchemy()
with open("current_properties.txt") as f:
    props = json.load(f)
    CURRENT_DATE = datetime.fromisoformat(props["current_date"])
    INITIALISE_FIXTURES = (
        props["initialise_fixtures"] == "true"
    )  # default to false if not set or cant be read!!
    PRODUCTION_ENVIRONMENT = (
        props["environment"] == "production"
    )  # default to false if not set or cant be read!!


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "9OLWxND4o83j4K4iuopO"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    # app.config["SQLALCHEMY_ECHO"] = True  # for debugging
    db_access.init_app(app)
    with app.app_context():
        from .prediction_model import PredictionModel
        from .fixture import Fixture
        from .player_prediction import PlayerPrediction

        if INITIALISE_FIXTURES:
            PlayerPrediction.__table__.drop(db_access.engine)
            Fixture.__table__.drop(db_access.engine)
        db_access.create_all()
        if INITIALISE_FIXTURES:
            FixtureCreator(db_access).create_fixtures()
        PredictionModel(db_access).calculate_predictions()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        from .user import User

        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    with app.app_context():
        from .fantleague import fantleague as main_blueprint

    app.register_blueprint(main_blueprint)
    return app
