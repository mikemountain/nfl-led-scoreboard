import json
import os

import debug
# from data import status
from data.config.layout import Layout
from utils import deep_update

SCROLLING_SPEEDS = [0.3, 0.2, 0.1, 0.075, 0.05, 0.025, 0.01]
DEFAULT_SCROLLING_SPEED = 2
DEFAULT_ROTATE_RATE = 15.0
MINIMUM_ROTATE_RATE = 2.0
DEFAULT_ROTATE_RATES = {"live": DEFAULT_ROTATE_RATE, "final": DEFAULT_ROTATE_RATE, "pregame": DEFAULT_ROTATE_RATE}
DEFAULT_PREFERRED_TEAMS = ["BUF"]
DEFAULT_PREFERRED_DIVISIONS = ["AFC East"]


class Config:
    def __init__(self, filename_base, width, height):
        json = self.__get_config(filename_base)

        # Preferred Teams/Divisions
        self.preferred_teams = json["preferred"]["teams"]
        self.preferred_divisions = json["preferred"]["divisions"]

        # Rotation
        self.rotation_enabled = json["rotation"]["enabled"]
        self.rotation_scroll_until_finished = json["rotation"]["scroll_until_finished"]
        self.rotation_only_preferred = json["rotation"]["only_preferred"]
        self.rotation_only_live = json["rotation"]["only_live"]
        self.rotation_rates = json["rotation"]["rates"]
        self.rotation_preferred_team_live_enabled = json["rotation"]["while_preferred_team_live"]["enabled"]

        # Misc config options
        self.time_format = json["time_format"]
        self.end_of_day = json["end_of_day"]
        self.debug = json["debug"]
        self.demo_date = json["demo_date"]
        self.helmet_logos = json["use_helmet_logos"]
        # Make sure the scrolling speed setting is in range so we don't crash
        try:
            self.scrolling_speed = SCROLLING_SPEEDS[json["scrolling_speed"]]
        except IndexError:
            debug.warning(
                "Scrolling speed should be an integer between 0 and 6. Using default value of {}".format(
                    DEFAULT_SCROLLING_SPEED
                )
            )
            self.scrolling_speed = SCROLLING_SPEEDS[DEFAULT_SCROLLING_SPEED]

        # Get the layout info
        json = self.__get_layout(width, height)
        self.layout = Layout(json, width, height)

        # Check the preferred teams and divisions are a list or a string
        self.check_time_format()
        self.check_preferred_teams()
        self.check_preferred_divisions()

        # Check the rotation_rates to make sure it's valid and not silly
        self.check_rotate_rates()

    def check_preferred_teams(self):
        if not isinstance(self.preferred_teams, str) and not isinstance(self.preferred_teams, list):
            debug.warning(
                "preferred_teams should be an array of team names or a single team name string."
                "Using default preferred_teams, {}".format(DEFAULT_PREFERRED_TEAMS)
            )
            self.preferred_teams = DEFAULT_PREFERRED_TEAMS
        if isinstance(self.preferred_teams, str):
            team = self.preferred_teams
            self.preferred_teams = [team]

    def check_preferred_divisions(self):
        if not isinstance(self.preferred_divisions, str) and not isinstance(self.preferred_divisions, list):
            debug.warning(
                "preferred_divisions should be an array of division names or a single division name string."
                "Using default preferred_divisions, {}".format(DEFAULT_PREFERRED_DIVISIONS)
            )
            self.preferred_divisions = DEFAULT_PREFERRED_DIVISIONS
        if isinstance(self.preferred_divisions, str):
            division = self.preferred_divisions
            self.preferred_divisions = [division]

    def check_time_format(self):
        if self.time_format.lower() == "24h":
            self.time_format = "%H"
        else:
            self.time_format = "%-I"

    def check_rotate_rates(self):
        if not isinstance(self.rotation_rates, dict):
            try:
                rate = float(self.rotation_rates)
                self.rotation_rates = {"live": rate, "final": rate, "pregame": rate}
            except:
                debug.warning(
                    "rotation_rates should be a Dict or Float. Using default value. {}".format(DEFAULT_ROTATE_RATES)
                )
                self.rotation_rates = DEFAULT_ROTATE_RATES

        for key, value in list(self.rotation_rates.items()):
            try:
                # Try and cast whatever the user passed into a float
                rate = float(value)
                self.rotation_rates[key] = rate
            except:
                # Use the default rotate rate if it fails
                debug.warning(
                    'Unable to convert rotate_rates["{}"] to a Float. Using default value. ({})'.format(
                        key, DEFAULT_ROTATE_RATE
                    )
                )
                self.rotation_rates[key] = DEFAULT_ROTATE_RATE

            if self.rotation_rates[key] < MINIMUM_ROTATE_RATE:
                debug.warning(
                    'rotate_rates["{}"] is too low. Please set it greater than {}. Using default value. ({})'.format(
                        key, MINIMUM_ROTATE_RATE, DEFAULT_ROTATE_RATE
                    )
                )
                self.rotation_rates[key] = DEFAULT_ROTATE_RATE

        # Setup some nice attributes to make sure they all exist
        self.rotation_rates_live = self.rotation_rates.get("live", DEFAULT_ROTATE_RATES["live"])
        self.rotation_rates_final = self.rotation_rates.get("final", DEFAULT_ROTATE_RATES["final"])
        self.rotation_rates_pregame = self.rotation_rates.get("pregame", DEFAULT_ROTATE_RATES["pregame"])

    def rotate_rate_for_status(self, game_status):
        rotate_rate = self.rotation_rates_live
        if status.is_pregame(game_status):
            rotate_rate = self.rotation_rates_pregame
        if status.is_complete(game_status):
            rotate_rate = self.rotation_rates_final
        return rotate_rate

    def read_json(self, path):
        """
        Read a file expected to contain valid json.
        If file not present return empty data.
        Exception if json invalid.
        """
        j = {}
        if os.path.isfile(path):
            j = json.load(open(path))
        else:
            debug.warning(f"Could not find json file {path}.  Skipping.")
        return j

    # example config is a "base config" which always gets read.
    # our "custom" config contains overrides.
    def __get_config(self, base_filename):
        filename = "{}.json".format(base_filename)
        reference_filename = "config.json.example"  # always use this filename.
        reference_config = self.read_json(reference_filename)
        custom_config = self.read_json(filename)
        if custom_config:
            new_config = deep_update(reference_config, custom_config)
            return new_config
        return reference_config
