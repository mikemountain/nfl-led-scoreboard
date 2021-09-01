from utils import get_file
import json
import os

DEFAULT_PREFERRED_TEAMS = ["NE", "NO"]
DEFAULT_PREFERRED_DIVISIONS = ["AFCW"]

class ScoreboardConfig:
    def __init__(self, filename_base, args):
        json = self.__get_config(filename_base)

        # Preferred Teams/Divisions
        self.preferred_teams = json["preferred"]["teams"]
        self.preferred_divisions = json["preferred"]["divisions"]

        # Rotation
        self.rotation_enabled = json["rotation"]["enabled"]
        self.rotation_only_preferred = json["rotation"]["only_preferred"]
        self.rotation_rates = json["rotation"]["rates"]
        self.rotation_preferred_team_live_enabled = json["rotation"]["while_preferred_team_live"]["enabled"]
        self.rotation_preferred_team_live_halftime = json["rotation"]["while_preferred_team_live"]["during_halftime"]

        # Debug
        self.debug = json["debug"]

        # Check if these are lists or strings
        self.check_preferred_teams()
        self.check_preferred_divisions()

    def check_preferred_teams(self):
        if not isinstance(self.preferred_teams, str) and not isinstance(self.preferred_teams, list):
            debug.warning("preferred_teams should be an array of team names or a single team name string. Using default preferred_teams, {}".format(DEFAULT_PREFERRED_TEAMS))
            self.preferred_teams = DEFAULT_PREFERRED_TEAMS
        if isinstance(self.preferred_teams, str):
            team = self.preferred_teams
            self.preferred_teams = [team]

    def check_preferred_divisions(self):
        if not isinstance(self.preferred_divisions, str) and not isinstance(self.preferred_divisions, list):
            debug.warning("preferred_divisions should be an array of division names or a single division name string. Using default preferred_divisions, {}".format(DEFAULT_PREFERRED_DIVISIONS))
            self.preferred_divisions = DEFAULT_PREFERRED_DIVISIONS
        if isinstance(self.preferred_divisions, str):
            division = self.preferred_divisions
            self.preferred_divisions = [division]

    def read_json(self, filename):
        # Find and return a json file

        j = {}
        path = get_file(filename)
        if os.path.isfile(path):
            j = json.load(open(path))
        return j

    def __get_config(self, base_filename):
        # Look and return config.json file

        filename = "{}.json".format(base_filename)
        reference_config = self.read_json(filename)

        return reference_config
