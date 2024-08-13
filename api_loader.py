from .loader import ResultLoader

from .time_property import current_time_property


class APIResultLoader(ResultLoader):

    def __init__(self) -> None:
        time_prop = current_time_property()
        self.season = time_prop.season
        self.game_week = time_prop.game_week

    # get all the api data. this wll be pretty static as its not the rugby season but we can use it to generate future fixtures by mangling data
    def get_historic_results_to_date(self) -> list:
        pass

    def is_result_before_date(self, result):
        pass

    # for testing we need to simulate different points in the season to see prediction and past date points
    def get_season_results_to_date(self) -> list:
        pass
