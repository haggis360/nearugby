from datetime import datetime


class TeamResult:

    def __init__(self, season: int, date: datetime, 
                 game_week: int, home: str, away: str, 
                 venue: str, home_score: int, away_score: int):
        self.seaason = season
        self.fixture_date = datetime.fromisoformat(date)
        self.game_week = game_week
        self.home_team = home
        self.away_team = away
        self.venue = venue
        self.home_score = home_score
        self.away_score = away_score
        if self.home_score == self.away_score:
            self.home_result = "D"
            self.away_result = "D"
        elif self.away_score > self.home_score:
            self.away_result = "W"
            self.home_result = "L"
        else:
            self.home_result = "W"
            self.away_result = "L"

    def __str__(self) -> str:
        return "Home Team: "+self.home_team
