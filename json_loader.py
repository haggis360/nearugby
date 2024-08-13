import json

from .loader import ResultLoader

from .time_property import current_time_property


class JsonResultLoader(ResultLoader):

    RESULT = "Result"  # constants in single location perhaps these should be in the properties class
    # COMP_NAME = ["T14", "TOP 14", "TOP14"]#dirty data that we have to provide tolerance for

    def __init__(self) -> None:
        time_prop = current_time_property()
        self.season = time_prop.season
        self.game_week = time_prop.game_week

    def reload_time_prop(self) -> None:
        time_prop = current_time_property()
        self.season = time_prop.season
        self.game_week = time_prop.game_week

    # get all the api data. this wll be pretty static as its not the rugby season but we can use it to generate future fixtures by mangling data
    def get_historic_results_to_date(self) -> list:
        # load all the files in the directory upto current date store as all_historic_results
        # get time property and loop the files less than or equal ro season to load
        self.reload_time_prop()
        full_history_db = []
        for season in range(2011, 2024):
            fixtures_file = "data/" + str(season) + ".json"
            with open(fixtures_file) as f:
                temp = json.load(f)
                ress = list(filter(self.is_result_before_date, temp["results"]))
                full_history_db = full_history_db + ress
        return full_history_db

    def is_result_before_date(self, result):
        # put this somewhere eles a query is run for every result!!!!!!!!!!
        #   prop = current_time_property()
        season = int(result["season"])
        g_week = int(result["game_week"])
        #   comp = result["comp_name"] retrieved by compid now so this not elevant
        # status = result["status"]
        return season < self.season or (
            season == self.season and g_week < self.game_week
        )  # and (status == JsonResultLoader.RESULT)

    # for testing we need to simulate different points in the season to see prediction and past date points
    def get_season_results_to_date(self) -> list:
        self.reload_time_prop()
        fixtures_file = "data/" + str(self.season) + ".json"
        with open(fixtures_file) as f:
            temp = json.load(f)
            ress = list(filter(self.is_result_before_date, temp["results"]))
            return ress

    # never do this - our api is read only. we cache tthe results to a file but pretend these dont exist
    # def save_db():
    #    with open("data/rugby__data_db.json", 'w') as f:
    #        return json.dump(db, f)

    # ncall fixtures api limit requests 10pday so cache in files
