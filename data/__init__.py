import time

import data.config.layout as layout
import debug
from data import status
from data.game import Game
from data.schedule import Schedule
from data.scoreboard import Scoreboard
from data.scoreboard.postgame import Postgame
from data.scoreboard.pregame import Pregame
from data.update import UpdateStatus


class Data:
    def __init__(self, config):
        # Save the parsed config
        self.config = config

        # get schedule
        self.schedule: Schedule = Schedule(config)

        self.current_game: Game = self.schedule.get_preferred_game()
        self.game_changed_time = time.time()

        # RENDER ITEMS
        self.scrolling_finished: bool = False

    def should_rotate_to_next_game(self):
        game = self.current_game
        if not self.config.rotation_enabled:
            return False

        stay_on_preferred_team = self.config.preferred_teams and not self.config.rotation_preferred_team_live_enabled
        if not stay_on_preferred_team:
            return True

        if self.schedule.num_games() < 2:
            if self.config.rotation_only_live and self.schedule.games_live():
                # don't want to get stuck on an dead game
                return not status.is_live(game.status())
            return False

        if game.features_team(self.config.preferred_teams[0]) and status.is_live(game.status()):
            if self.config.rotation_preferred_team_live_mid_inning and status.is_inning_break(game.inning_state()):
                return True
            return False

        return True

    def refresh_game(self):
        status = self.current_game.update()
        if status == UpdateStatus.SUCCESS:
            self.__update_layout_state()
            self.print_game_data_debug()
            self.network_issues = False
        elif status == UpdateStatus.FAIL:
            self.network_issues = True

    def advance_to_next_game(self):
        game = self.schedule.next_game()
        if game is not None:
            if game.game_id != self.current_game.game_id:
                self.game_changed_time = time.time()
            self.current_game = game
            self.__update_layout_state()
            self.print_game_data_debug()
            self.network_issues = False

        else:
            self.network_issues = True

    def refresh_schedule(self, force=False):
        self.__process_network_status(self.schedule.update(force))

    def __process_network_status(self, status):
        if status == UpdateStatus.SUCCESS:
            self.network_issues = False
        elif status == UpdateStatus.FAIL:
            self.network_issues = True

    def get_screen_type(self):
        # Preferred Teams on BYE?
        # just return games for now, work on next things later
        return "games"

    def __update_layout_state(self):
        # pre/live/post game stuff
        self.config.layout.set_state()

    def print_game_data_debug(self):
        debug.log("Game Data Refreshed: %s",
                  self.current_game._data["gameData"]["game"]["id"])
        debug.log("Pre: %s", Pregame(
            self.current_game, self.config.time_format))
        debug.log("Live: %s", Scoreboard(self.current_game))
        debug.log("Final: %s", Postgame(self.current_game))
