import time
import re
from datetime import datetime

import debug
import api

GAME_UPDATE_RATE = 10

class Game:
    def __init__(self, game_id, date):
        self.game_id = game_id
        self.date = date.strftime("%Y-%m-%d")
        self.starttime = time.time()
        self._data = {}

    def update(self, force=False):
        if force or self.__should_update():
            self.starttime = time.time()
            try:
                debug.log("Fetching data for game %s", str(self.game_id))
                self._data = api.get_game(self.game_id)
            except:
                debug.exception("API error, failed to get game info for game %s", str(self.game_id))
                return "fail"

    def datetime(self):
        time = self._data['date']
        return datetime.fromisoformat(time.replace('Z', ''))

    def home_name(self):
        pass
    
    def home_abbr(self):
        return self._data['home_abbr']

    def away_name(self):
        pass

    def away_abbr(self):
        return self._data['away_abbr']

    def state(self):
        return self._data['state']

    def home_score(self):
        return self._data['home_score']

    def away_score(self):
        return self._data['away_score']

    def winning_team(self):
        pass

    def losing_team(self):
        pass

    def quarter_state(self):
        pass
    
    def quarter_number(self):
        return self._data['quarter']

    def redzone(self):
        return self._data['redzone']

    def down_number(self):
        down = self._data['down']
        return re.sub(r'[a-z]+', '', down).replace(' ', '')
    
    def yards_to_gain(self):
        return self._data['spot'].replace(' ', '')

    def time_on_clock(self):
        return self._data['time']

    def possession(self):
        return self._data['possession']

    def __should_update(self):
        endtime = time.time()
        time_delta = endtime - self.starttime
        return time_delta >= GAME_UPDATE_RATE