import time
from datetime import datetime, timedelta

import debug
import data.api as api
from data.game import Game

SCHEDULE_REFRESH_RATE = 6 * 60

class Schedule:
    def __init__(self, config):
        self.config = config
        self.week = self.__get_week()
        self.season_type = self.__get_season_type()
        self.starttime = time.time()
        self.current_idx = 0
        self.preferred_over = False
        self.__all_games = []
        self._games = []
        self.update(True)

    def __get_week(self):
        return api.get_week()
    
    def __get_season_type():
        return api.get_season_type()

    def update(self, force=False):
        if force or self.__should_update():
            self.week = self.__get_week()
            debug.log('Updating schedule for week %s', self.week)
            self.starttime = time.time()
            try:
                self.__all_games = api.get_game_ids()
            except:
                debug.exception('Network error while trying to refresh schedule')
            else:
                self._games = self.__all_games
                if self.config.rotation_only_preferred:
                    self._games = Schedule.__filter_list_of_games(self.__all_games, self.config.preferred_teams)
                if self.config.rotation_only_live:
                    games = [g for g in self._games if g['status'] == 'in']
                    if games:
                        self._games = games

    
    def __should_update(self):
        endtime = time.time()
        return endtime - self.starttime >= SCHEDULE_REFRESH_RATE

    # def is_bye_week_for_preferred_teams(self):
    #     bye_week = False
    #     if self.config.preferred_teams:
    #         for t in self.config.preferred_teams:
    #             bye_week = not any(t in [game['home_abbr'], game['away_abbr']] for game in self.__all_games)
    #     return bye_week

    def num_games(self):
        return len(self._games)