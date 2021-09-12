from datetime import datetime, timedelta
import time as t
import nfl_api_parser as nflparser
import debug

NETWORK_RETRY_SLEEP_TIME = 10.0

class Data:
    def __init__(self, config):
        # Save the parsed config
        self.config = config

        # Flag to determine when to refresh data
        self.needs_refresh = True

        self.helmet_logos = self.config.helmet_logos
        
        # Parse today's date and see if we should use today or yesterday
        self.get_current_date()
        # Fetch the teams info
        self.refresh_games()

        # self.playoffs = nflparser.is_playoffs()
        # self.games = nflparser.get_all_games()
        # self.game = self.choose_game()
        # self.gametime = self.get_gametime()

        # What game do we want to start on?
        self.current_game_index = 0
        self.current_division_index = 0
        # self.scores = {}

    def get_current_date(self):
        return datetime.utcnow()
    
    def refresh_game(self):
        self.game = self.choose_game()
        self.needs_refresh = False

    def refresh_games(self):
        attempts_remaining = 5
        while attempts_remaining > 0:
            try:
                all_games = nflparser.get_all_games()
                if self.config.rotation_only_preferred:
                    self.games = self.__filter_list_of_games(all_games, self.config.preferred_teams)
                # if rotation is disabled, only look at the first team in the list of preferred teams
                elif not self.config.rotation_enabled:
                    self.games = self.__filter_list_of_games(all_games, [self.config.preferred_teams[0]])
                else:
                    self.games = all_games

                self.games_refresh_time = t.time()
                self.network_issues = False
                break
            except Exception as e:
                self.network_issues = True
                debug.error("Networking error while refreshing the master list of games. {} retries remaining.".format(attempts_remaining))
                debug.error("Exception: {}".format(e))
                attempts_remaining -= 1
                t.sleep(NETWORK_RETRY_SLEEP_TIME)
            except ValueError:
                self.network_issues = True
                debug.error("Value Error while refreshing master list of games. {} retries remaining.".format(attempts_remaining))
                debug.error("ValueError: Failed to refresh list of games")
                attempts_remaining -= 1
                t.sleep(NETWORK_RETRY_SLEEP_TIME)

    #     # If we run out of retries, just move on to the next game
        if attempts_remaining <= 0 and self.config.rotation_enabled:
            self.advance_to_next_game()

    def get_gametime(self):
        tz_diff = t.timezone if (t.localtime().tm_isdst == 0) else t.altzone
        gametime = datetime.strptime(self.games[self.current_game_index]['date'], "%Y-%m-%dT%H:%MZ") + timedelta(hours=(tz_diff / 60 / 60 * -1))
        return gametime

    def current_game(self):
        return self.games[self.current_game_index]

    # def update_scores(self, homescore, awayscore):
    #     self.scores[self.current_game_index] = {'home': homescore, 'away': awayscore}

    # def get_current_scores(self):
    #     if self.scores[self.current_game_index]:
    #         return self.scores[self.current_game_index]
    #     else:
    #         return {'home': 0, 'away': 0}

    # def refresh_overview(self):
    #     attempts_remaining = 5
    #     while attempts_remaining > 0:
    #         try:
    #             self.__update_layout_state()
    #             self.needs_refresh = False
    #             self.print_overview_debug()
    #             self.network_issues = False
    #             break
    #         except URLError, e:
    #             self.network_issues = True
    #             debug.error("Networking Error while refreshing the current overview. {} retries remaining.".format(attempts_remaining))
    #             debug.error("URLError: {}".format(e.reason))
    #             attempts_remaining -= 1
    #             time.sleep(NETWORK_RETRY_SLEEP_TIME)
    #         except ValueError:
    #             self.network_issues = True
    #             debug.error("Value Error while refreshing current overview. {} retries remaining.".format(attempts_remaining))
    #             debug.error("ValueError: Failed to refresh overview for {}".format(self.current_game().game_id))
    #             attempts_remaining -= 1
    #             time.sleep(NETWORK_RETRY_SLEEP_TIME)

    #     # If we run out of retries, just move on to the next game
    #     if attempts_remaining <= 0 and self.config.rotation_enabled:
    #         self.advance_to_next_game()

    def advance_to_next_game(self):
        self.current_game_index = self.__next_game_index()
        return self.current_game()

    # def game_index_for_preferred_team(self):
    #     if self.config.preferred_teams:
    #         return self.__game_index_for(self.config.preferred_teams[0])
    #     else:
    #         return 0

    def __filter_list_of_games(self, games, teams):
        return list(game for game in games if set([game['awayteam'], game['hometeam']]).intersection(set(teams)))

    # def __game_index_for(self, team_name):
    #     team_index = 0
    #     print(self.games)
    #     # team_idxs = [i for i, game in enumerate(self.games) if team_name in [game.awayteam, game.hometeam]]
    #     for game in enumerate(self.games):
    #         print(game)
    #     return team_index

    def __next_game_index(self):
        counter = self.current_game_index + 1
        if counter >= len(self.games):
            counter = 0
        return counter

    #
    # Debug info

    # def print_overview_debug(self):
    #     debug.log("Overview Refreshed: {}".format(self.overview.id))
    #     debug.log("Pre: {}".format(Pregame(self.overview, self.config.time_format)))
    #     debug.log("Live: {}".format(Scoreboard(self.overview)))
    #     debug.log("Final: {}".format(Final(self.current_game())))