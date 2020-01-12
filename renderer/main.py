from PIL import Image, ImageFont, ImageDraw, ImageSequence
from rgbmatrix import graphics
from utils import center_text
from calendar import month_abbr
from renderer.screen_config import screenConfig
from datetime import datetime, timedelta
import time as t
import debug

class MainRenderer:
    def __init__(self, matrix, data):
        self.matrix = matrix
        self.data = data
        self.screen_config = screenConfig("64x32_config")
        self.canvas = matrix.CreateFrameCanvas()
        self.width = 64
        self.height = 32
        # Create a new data image.
        self.image = Image.new('RGB', (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)
        # Load the fonts
        self.font = ImageFont.truetype("fonts/score_large.otf", 16)
        self.font_mini = ImageFont.truetype("fonts/04B_24__.TTF", 8)

    def render(self):
        # we're in turbo lazy playoff mode right now don't @ me
        while True:
            self.data.get_current_date()
            if self.data.game['state'] == "in":
                self._draw_game()
            else:
                self.__render_game()

    def __render_game(self):
        time = self.data.get_current_date()
        gametime = datetime.strptime(self.data.game['date'], "%Y-%m-%dT%H:%MZ")
        if time < gametime - timedelta(hours=2) and self.data.game['state'] == 'pre':
            debug.info('Scheduled State, waiting 30')
            self._draw_pregame()
            t.sleep(1800)
        elif time < gametime - timedelta(hours=1) and self.data.game['state'] == 'pre':
            debug.info('Pre-Game State, waiting 1 minute')
            self._draw_pregame()
            t.sleep(60)
        elif self.data.game['state'] == 'post':
            debug.info('Final State, waiting 6 hours')
            self._draw_post_game()
            t.sleep(3600)
        else:
            debug.info('Live State, checking every 5s')
            self._draw_game()
        debug.info('ping render_game')

    def __render_off_day(self):
        debug.info('ping_day_off')
        self._draw_off_day()
        t.sleep(21600) #sleep 6 hours

    def _draw_pregame(self):
        if self.data.game != 0:
            overview = self.data.game
            gametime = self.data.gametime
            # Center the game time on screen.
            gametime_pos = center_text(self.font_mini.getsize(gametime)[0], 32)
            # Set the position of each logo
            # I haven't manually set this stuff yet so they're all gonna use #1
            # away_team_logo_pos = self.screen_config.team_logos_pos[str(overview['awayteam'])]['away']
            # home_team_logo_pos = self.screen_config.team_logos_pos[str(overview['hometeam'])]['home']
            away_team_logo_pos = self.screen_config.team_logos_pos["1"]['away']
            home_team_logo_pos = self.screen_config.team_logos_pos["1"]['home']
            # Open the logo image file
            away_team_logo = Image.open('logos/{}.png'.format(overview['awayteam'])).resize((23, 23), 1)
            home_team_logo = Image.open('logos/{}.png'.format(overview['hometeam'])).resize((23, 23), 1)
            # Draw the text on the Data image.
            self.draw.text((22, -1), 'TODAY', font=self.font_mini)
            self.draw.multiline_text((gametime_pos, 5), gametime, fill=(255, 255, 255), font=self.font_mini, align="center")
            self.draw.text((25, 13), 'VS', font=self.font)
            # Put the data on the canvas
            self.canvas.SetImage(self.image, 0, 0)
            # Put the images on the canvas
            self.canvas.SetImage(away_team_logo.convert("RGB"), away_team_logo_pos["x"] + 13, away_team_logo_pos["y"] + 11)
            self.canvas.SetImage(home_team_logo.convert("RGB"), home_team_logo_pos["x"] - 8, home_team_logo_pos["y"] + 11)
            # Load the canvas on screen.
            self.canvas = self.matrix.SwapOnVSync(self.canvas)
            # Refresh the Data image.
            self.image = Image.new('RGB', (self.width, self.height))
            self.draw = ImageDraw.Draw(self.image)
        else:
            #(Need to make the screen run on it's own) If connection to the API fails, show bottom red line and refresh in 1 min.
            self.draw.line((0, 0) + (self.width, 0), fill=128)
            self.canvas = self.matrix.SwapOnVSync(self.canvas)
            t.sleep(60)  # sleep for 1 min
            # Refresh canvas
            self.image = Image.new('RGB', (self.width, self.height))
            self.draw = ImageDraw.Draw(self.image)

    def _draw_game(self):
        # self.data.refresh_game()
        overview = self.data.game
        homescore = overview['homescore']
        awayscore = overview['awayscore']
        while True:
            # Refresh the data
            if self.data.needs_refresh:
                debug.info('Refresh game overview')
                self.data.refresh_game()
                self.data.needs_refresh = False
            if self.data.game != 0:
                overview = self.data.game
                # Use This code if you want the goal animation to run only for your fav team's goal
                # if self.data.fav_team_id == overview['hometeam']:
                #     if overview['homescore'] > homescore:
                #         self._draw_goal()
                # else:
                #     if overview['awayscore'] > awayscore:
                #         self._draw_goal()
                # Use this code if you want the goal animation to run for both team's goal.
                # Run the goal animation if there is a goal.
                if overview['homescore'] > homescore or overview['awayscore'] > awayscore:
                   self._draw_goal()
                # Prepare the data
                print(overview['quarter'], overview['time'])
                score = '{}-{}'.format(overview['awayscore'], overview['homescore'])
                quarter = str(overview['quarter'])
                time_period = overview['time']
                # Set the position of the information on screen.
                time_period_pos = center_text(self.font_mini.getsize(time_period)[0], 32)
                score_position = center_text(self.font.getsize(score)[0], 32)
                quarter_position = center_text(self.font_mini.getsize(quarter)[0], 32)
                # Set the position of each logo on screen.
                # I haven't manually set this stuff yet so they're all gonna use #1
                # away_team_logo_pos = self.screen_config.team_logos_pos[str(overview['awayteam'])]['away']
                # home_team_logo_pos = self.screen_config.team_logos_pos[str(overview['hometeam'])]['home']
                away_team_logo_pos = self.screen_config.team_logos_pos["1"]['away']
                home_team_logo_pos = self.screen_config.team_logos_pos["1"]['home']
                # Open the logo image file
                away_team_logo = Image.open('logos/{}.png'.format(overview['awayteam'])).resize((23, 23), 1)
                home_team_logo = Image.open('logos/{}.png'.format(overview['hometeam'])).resize((23, 23), 1)
                # Draw the text on the Data image.
                self.draw.multiline_text((score_position, 19), score, fill=(255, 255, 255), font=self.font, align="center")
                self.draw.multiline_text((quarter_position, -1), quarter, fill=(255, 255, 255), font=self.font_mini, align="center")
                self.draw.multiline_text((time_period_pos, 5), time_period, fill=(255, 255, 255), font=self.font_mini, align="center")
                # Put the data on the canvas
                self.canvas.SetImage(self.image, 0, 0)
                # Put the images on the canvas
                self.canvas.SetImage(away_team_logo.convert("RGB"), away_team_logo_pos["x"] + 13, away_team_logo_pos["y"] - 3)
                self.canvas.SetImage(home_team_logo.convert("RGB"), home_team_logo_pos["x"] - 8, home_team_logo_pos["y"] - 5)
                # Load the canvas on screen.
                self.canvas = self.matrix.SwapOnVSync(self.canvas)
                # Refresh the Data image.
                self.image = Image.new('RGB', (self.width, self.height))
                self.draw = ImageDraw.Draw(self.image)
                # Check if the game is over
                if overview['state'] == 'post':
                    debug.info('GAME OVER')
                    break
                # Save the scores.
                awayscore = overview['awayscore']
                homescore = overview['homescore']
                self.data.needs_refresh = True
                t.sleep(5)
            else:
                # (Need to make the screen run on it's own) If connection to the API fails, show bottom red line and refresh in 1 min.
                self.draw.line((0, 0) + (self.width, 0), fill=128)
                self.canvas = self.matrix.SwapOnVSync(self.canvas)
                t.sleep(60)  # sleep for 1 min

    def _draw_post_game(self):
        self.data.refresh_game()
        if self.data.game != 0:
            overview = self.data.game
            # Prepare the data
            game_date = '{} {}'.format(month_abbr[self.data.month], self.data.day)
            score = '{}-{}'.format(overview['awayscore'], overview['homescore'])
            time_period = overview['time']
            # Set the position of the information on screen.
            game_date_pos = center_text(self.font_mini.getsize(game_date)[0], 32)
            time_period_pos = center_text(self.font_mini.getsize(time_period)[0], 32)
            score_position = center_text(self.font.getsize(score)[0], 32)
            # Draw the text on the Data image.
            away_team_logo_pos = self.screen_config.team_logos_pos["1"]['away']
            home_team_logo_pos = self.screen_config.team_logos_pos["1"]['home']
            # Open the logo image file
            away_team_logo = Image.open('logos/{}.png'.format(overview['awayteam'])).resize((23, 23), 1)
            home_team_logo = Image.open('logos/{}.png'.format(overview['hometeam'])).resize((23, 23), 1)
            # Draw the text on the Data image.
            self.draw.multiline_text((score_position, 19), score, fill=(255, 255, 255), font=self.font, align="center")
            self.draw.multiline_text((quarter_position, -1), quarter, fill=(255, 255, 255), font=self.font_mini, align="center")
            self.draw.multiline_text((time_period_pos, 5), time_period, fill=(255, 255, 255), font=self.font_mini, align="center")
            # Put the data on the canvas
            self.canvas.SetImage(self.image, 0, 0)
            # Put the images on the canvas
            self.canvas.SetImage(away_team_logo.convert("RGB"), away_team_logo_pos["x"] + 13, away_team_logo_pos["y"] - 3)
            self.canvas.SetImage(home_team_logo.convert("RGB"), home_team_logo_pos["x"] - 8, home_team_logo_pos["y"] - 5)
            # Load the canvas on screen.
            self.canvas = self.matrix.SwapOnVSync(self.canvas)
            # Refresh the Data image.
            self.image = Image.new('RGB', (self.width, self.height))
            self.draw = ImageDraw.Draw(self.image)
        else:
            # (Need to make the screen run on it's own) If connection to the API fails, show bottom red line and refresh in 1 min.
            self.draw.line((0, 0) + (self.width, 0), fill=128)
            self.canvas = self.matrix.SwapOnVSync(self.canvas)
            t.sleep(60)  # sleep for 1 min

    def _draw_goal(self):
        debug.info('SCOOOOOOOORE, MAY DAY, MAY DAY, MAY DAY, MAY DAAAAAAAAY - Rick Jeanneret')
        # Load the gif file
        im = Image.open("Assets/goal_light_animation.gif")
        # Set the frame index to 0
        frameNo = 0
        self.canvas.Clear()
        # Go through the frames
        x = 0
        while x is not 5:
            try:
                im.seek(frameNo)
            except EOFError:
                x += 1
                frameNo = 0
                im.seek(frameNo)
            self.canvas.SetImage(im.convert('RGB'), 0, 0)
            self.canvas = self.matrix.SwapOnVSync(self.canvas)
            frameNo += 1
            t.sleep(0.1)

    def _draw_off_day(self):
        self.draw.text((0, -1), 'NO GAME TODAY', font=self.font_mini)
        self.canvas.SetImage(self.image, 0, 0)
        self.canvas = self.matrix.SwapOnVSync(self.canvas)