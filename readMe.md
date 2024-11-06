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
or windows 
set FLASK_APP=.
set FLASK_DEBUG=1

then:
flask run

this also initialisies the db - on my machine its saved to /Users/user/Documents/Martin/python/instance/db.sqlite

sample urls
http://127.0.0.1:5000/match_form/Stade%20Francais/Castres shows the latest match results between those 2 teams
http://127.0.0.1:5000/team_form/Toulouse shows the latest results for a team
http://127.0.0.1:5000/add_prediction/2022/9 shows the predictions entered or available for a season and gameweek. retreieves predictions for the fixtures if they have been created for that user otherwise empty predictions which can be saved
http://127.0.0.1:5000/fixtures/2023/6 the fixtures for a season and week

these would need to be bottom windows of a prediction screen perhaps

run the file generate_script.py to generate the sql delete and insert statements for test users and a loaded set of predictions
it generates a script in init_users_predictions.txt which can be run in sql

there are 2 loaders use the property to deterins wheter to use the api loader - production or json loader of cached data for test/dev

this is a systems integraton project, it looks like a website but the overwhelming challenge is in the management and integraton of data. this is very important to me as i think its the most commeon and most important challenge in software engineering. data science and ai optimisation requires the integration of the massive amounts of data that have been collected and stored in diferent formats media and locations. then refining and restructuing this data for optimal use in a separate system. its a challenge as you have no control over the data stored in a 3rd party api or system and must make it work for you, you cannot change the question to what yu know the answer to. yuo must find the answer and this involves struggles i wanted to experience its very satisfying to crack the answers.
i had to cope with
data format - results and fixtures are not stored in the external api in the same way i needed to separate these into result, predictions and fixtures format
data quality - on reviewing data different values are used for the same keys in data eg top14, t14, top 14. this needed cleainng and was only apparent on inspecting
data volume - to give an effective league for real testing i needed to manipulate the current date to simulate different times in the year when fixtures had happened or not
data testing - i needed to generate some control data to test the season reults calculations
data demo - i needed to generate bulk data to show league table from many simulated users
api challenges - i had to 'cache' data into a file for season as api invocations were limited to a small number before occuring significatnt costs. the api model extrends a base class to allow either the eral api or the cahced data to be used. again this is a real world problem i had to solve which is simular to financial optimistation decisions companies made
logic/design - the challenge is in logic and design not in code. i had to plan what i wanted to show and display and work within the fixed constraints of the api data that i had available
data protection - i made the cached file data read only after initisling. this is to simulate the api nature of 3rd party which cannot be changed. all editable application data i stored in a separate system - a relational db . i had to systems integrate api to file to database (3 data repositories)
utility serives - property files allow the initialisation of loading fixture data.
roles - there are 3 roles . i designed for separate users and a fully functionang app which doesnt not need to ever be restarted all functionality run from within it
user stories - each role has different use cases available
public - can view only league tables
registered user - can enter predictions see their profile including lastes record form
admin user - can reset the current season and game week triggering league recalcations. this woldl nt be needed in a live system which would run continueously but is here for demo purposes
images for t4ams - stored in a dictionary, its static and hardcoded, a defulat provided for ones i couldnt find an image for
relational db - allows me to run queries for testing in the db and optimise them. let the db do the query work closer to the data source so minimal data is transferred between systems
security - i have encryoted the user passwords in db so that they aresnt visible to an admin (they could still be decrupted using the secret key if that was kniwn - in production id store that in a keystore)
security - sql injection to stop malicious sql statements on form input fields i used sql alchemay parameter replacement with typed parameters which encodes stringd passed in

structure
data- calling an ext api
data considerations
api invocation limitations
caching data in js0n
storing data in application db object types
mapping json api data to db tables
using sql alchemy orm to save
key queries
data initialisaton for testing
refreshing and reloading predictions algorithm to demonstrate over time
parameters used for fixtures
page routing - how it works in flask
roles - page filering -adding a second app with login match
demo with profile page
using a user library
use cases for roles
screens required
leage table view
calculating table positions - testing query in sql
recent player scores
drill through screens - using flask
updating predictions - using post
updating time - using admin post
showing latest matches
showing latest results
style
using html and stylesheets
image dictionary
menu layout
user evaluation
