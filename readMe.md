create a virtual environment using rugbyfl as the module name. creates bin, include and lib dirs and pyvenv.cfg file
python3 -m venv env

activate the environment to use the propertites
source env/bin/activate

first time install pip dependencies from requirements
pip install -r requirements.txt

when finished working in environment close it
deactivate

when developing and adding new dependencies
install required packages - eg:
pip install flask flask-sqlalchemy flask-login

then write to requirements.txt
pip freeze > requirements.txt

to run enter from terminal use . current dir for app so that the **init** is called to register the blueprints into the app
export FLASK_APP=.
export FLASK_DEBUG=1

then:
flask run

this also initialisies the db - on my machine its saved to /Users/user/Documents/Martin/python/instance/db.sqlite

sample urls
http://127.0.0.1:5000/match_form/Stade%20Francais/Castres shows the latest match results between those 2 teams
http://127.0.0.1:5000/team_form/Toulouse shows the latest results for a team

these would need to be bottom windows of a prediction screen perhaps
