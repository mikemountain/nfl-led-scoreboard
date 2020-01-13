from datetime import datetime, timedelta
import time as t
import nfl_api_parser as nflparser

class Data:
    def __init__(self, config):
        self.idex = 0
        # Save the parsed config
        self.config = config
        # Flag to determine when to refresh data
        self.needs_refresh = True
        # Flag to determine when it's a new day
        self.new_day = False
        # get favorite team's id
        self.fav_team = self.config.fav_team
        # Parse today's date and see if we should use today or yesterday
        self.get_current_date()
        # Fetch the teams info
        self.playoffs = nflparser.is_playoffs()
        self.games = nflparser.get_all_games()
        self.game = self.choose_game()
        self.gametime = self.get_gametime()

    def get_current_date(self):
        return datetime.utcnow()
    
    def refresh_game(self):
        self.game = self.choose_game()
        self.needs_refresh = False

    def choose_game(self):
        if self.playoffs:
            games = nflparser.get_all_games()
            return nflparser.which_playoff_game(games)
        else:
            return nflparser.get_game(self.fav_team)

    def get_gametime(self):
        tz_diff = t.timezone if (t.localtime().tm_isdst == 0) else t.altzone
        gametime = datetime.strptime(self.game['date'], "%Y-%m-%dT%H:%MZ") + timedelta(hours=(tz_diff / 60 / 60 * -1))
        return gametime.strftime("%-I:%M %p")

    # def refresh_fav_team_status(self):
    #     gametime = datetime.strptime(self.game.date, "%Y-%m-%dT%H:%MZ")
    #     self.fav_team_game_today = self.get_current_date >= gametime - timedelta(hours=24)
