import time
from typing import NoReturn

import debug
from data import Data, status
from data.scoreboard import Scoreboard
from data.scoreboard.postgame import Postgame
from data.scoreboard.pregame import Pregame
from renderer import network
from renderer.games import game as gamerender
from renderer.games import irregular
from renderer.games import postgame as postgamerender
from renderer.games import pregame as pregamerender
from renderer.games import teams


class MainRenderer:
    def __init__(self, matrix, data):
        self.matrix = matrix
        self.data: Data = data
        self.canvas = matrix.CreateFrameCanvas()
        self.scrolling_text_pos = self.canvas.width
        self.game_changed_time = time.time()
        self.animation_time = 0

    def render(self):
        refresh_rate = self.data.config.scrolling_speed

        while True:
            if self.game_changed_time < self.data.game_changed_time:
                self.scrolling_text_pos = self.canvas.width
                self.data.scrolling_finished = False
                self.game_changed_time = time.time()

            # Draw the current game
            self.__draw_game()

            # Check if we need to scroll until it's finished
            if not self.data.config.rotation_scroll_until_finished:
                self.data.scrolling_finished = True

            time.sleep(refresh_rate)

    # Draws the provided game on the canvas
    def __draw_game(self):
        game = self.data.current_game
        scoreboard = Scoreboard(game)
        layout = self.data.config.layout
        # teams.render_team_banner(
        #     self.canvas,
        #     layout,
        #     self.data.config.team_colors,
        #     scoreboard.home_team,
        #     scoreboard.away_team,
        #     self.data.config.full_team_names,
        #     self.data.config.short_team_names_for_runs_hits,
        # )

        if game.status() == 'pre':  # Draw the pregame information
            # self.__max_scroll_x(layout.coords("pregame.scrolling_text"))
            pregame = Pregame(game, self.data.config.time_format)
            pos = pregamerender.render_pregame(self.canvas, layout, pregame)
            self.__update_scrolling_text_pos(pos, self.canvas.width)

        elif status.is_complete(game.status()):  # Draw the game summary
            self.__max_scroll_x(layout.coords("final.scrolling_text"))
            final = Postgame(game)
            pos = postgamerender.render_postgame(
                self.canvas, layout, colors, final, scoreboard, self.scrolling_text_pos
            )

        elif status.is_irregular(game.status()):  # Draw game status
            short_text = self.data.config.layout.coords("status.text")[
                "short_text"]
            if scoreboard.get_text_for_reason():
                self.__max_scroll_x(layout.coords("status.scrolling_text"))
                pos = irregular.render_irregular_status(
                    self.canvas, layout, colors, scoreboard, short_text, self.scrolling_text_pos
                )
                self.__update_scrolling_text_pos(pos, self.canvas.width)
            else:
                irregular.render_irregular_status(
                    self.canvas, layout, colors, scoreboard, short_text)
                self.data.scrolling_finished = True

        else:  # draw a live game
            if scoreboard.homerun() or scoreboard.strikeout():
                self.animation_time += 1
            else:
                self.animation_time = 0

            loop_point = self.data.config.layout.coords("atbat")["loop"]
            self.scrolling_text_pos = min(self.scrolling_text_pos, loop_point)
            pos = gamerender.render_live_game(
                self.canvas, layout, colors, scoreboard, self.scrolling_text_pos, self.animation_time
            )
            self.__update_scrolling_text_pos(pos, loop_point)

        # Show network issues
        if self.data.network_issues:
            network.render_network_error(self.canvas, layout, colors)

        self.canvas = self.matrix.SwapOnVSync(self.canvas)
