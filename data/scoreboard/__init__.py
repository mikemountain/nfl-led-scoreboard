from data.game import Game
# from data.scoreboard.quarter import Quarter
# from data.scoreboard.possession import Possession
# from data.scoreboard.down import Down
# from data.scoreboard.yards import Yards
from data.scoreboard.team import Team


class Scoreboard:
    """Contains data for a current game.
    """

    def __init__(self, game: Game):
        self.away_team = Team(game.away_abbr(), game.away_score())
        self.home_team = Team(game.home_abbr(), game.home_score())
        # self.inning = Inning(game)
        # self.bases = Bases(game)
        # self.pitches = Pitches(game)
        # self.outs = Outs(game)
        self.game_status = game.status()
        # self.atbat = AtBat(game)

        # this can be implemented, events:competitions:situation:lastPlay:type:text
        # need to see it in live action though
        # self.play_result = game.current_play_result()

    # def touchdown(self):
    #     return self.play_result == "touchdown"

    # def field_goal(self):
    #     return self.play_result == "Field Goal Good"

    def __str__(self):
        s = (
            "<{} {}> {} ({}) @ {} ({}); Status: {};".format(
                self.__class__.__name__,
                hex(id(self)),
                self.away_team.abbrev,
                str(self.away_team.score),
                self.home_team.abbrev,
                str(self.home_team.score),
                self.game_status,
            )
        )
        return s
