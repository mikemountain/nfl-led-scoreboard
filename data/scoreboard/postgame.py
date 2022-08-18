from data.game import Game


class Postgame:
    def __init__(self, game: Game):
        self.winners = game.winning_team()
        self.losers = game.losing_team()

    def __str__(self):
        return "<{} {}> W: {}; L: {}".format(
            self.__class__.__name__,
            hex(id(self)),
            self.winners,
            self.losers,
        )
