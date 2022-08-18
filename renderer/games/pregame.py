try:
    from rgbmatrix import graphics
except ImportError:
    from RGBMatrixEmulator import graphics

from data.config.layout import Layout
from data.scoreboard.pregame import Pregame
# from renderer import scrollingtext
from utils import center_text_position

# fuckin do this later
def render_pregame(canvas, layout: Layout, pregame: Pregame):
    time = self.data.get_current_date()
    gamedatetime = self.data.get_gametime()
    if gamedatetime.day == time.day:
        date_text = 'TODAY'
    else:
        date_text = gamedatetime.strftime('%A %-d %b').upper()
    gametime = gamedatetime.strftime("%-I:%M %p")
    # Center the game time on screen.                
    date_pos = center_text(self.font_mini.getsize(date_text)[0], 32)
    gametime_pos = center_text(self.font_mini.getsize(gametime)[0], 32)
    # Draw the text on the Data image.
    self.draw.text((date_pos, 0), date_text, font=self.font_mini)
    self.draw.multiline_text((gametime_pos, 6), gametime, fill=(255, 255, 255), font=self.font_mini, align="center")
    self.draw.text((25, 15), 'VS', font=self.font)
    # Put the data on the canvas
    self.canvas.SetImage(self.image, 0, 0)
    if self.data.helmet_logos:
        # Open the logo image file
        away_team_logo = Image.open('logos/{}H.png'.format(game['awayteam'])).resize((20, 20), 1)
        home_team_logo = Image.open('logos/{}H.png'.format(game['hometeam'])).resize((20, 20), 1).transpose(Image.FLIP_LEFT_RIGHT)
        # Put the images on the canvas
        self.canvas.SetImage(away_team_logo.convert("RGB"), 1, 12)
        self.canvas.SetImage(home_team_logo.convert("RGB"), 43, 12)
    else:
        # TEMP Open the logo image file
        away_team_logo = Image.open('logos/{}.png'.format(game['awayteam'])).resize((20, 20), Image.BOX)
        home_team_logo = Image.open('logos/{}.png'.format(game['hometeam'])).resize((20, 20), Image.BOX)
        # Put the images on the canvas
        self.canvas.SetImage(away_team_logo.convert("RGB"), 1, 12)
        self.canvas.SetImage(home_team_logo.convert("RGB"), 43, 12)
        # awaysize = self.screen_config.team_logos_pos[game['awayteam']]['size']
        # homesize = self.screen_config.team_logos_pos[game['hometeam']]['size']
        # # Set the position of each logo
        # away_team_logo_pos = self.screen_config.team_logos_pos[game['awayteam']]['preaway']
        # home_team_logo_pos = self.screen_config.team_logos_pos[game['hometeam']]['prehome']
        # # Open the logo image file
        # away_team_logo = Image.open('logos/{}.png'.format(game['awayteam'])).resize((awaysize, awaysize), 1)
        # home_team_logo = Image.open('logos/{}.png'.format(game['hometeam'])).resize((homesize, homesize), 1)
        # # Put the images on the canvas
        # self.canvas.SetImage(away_team_logo.convert("RGB"), away_team_logo_pos["x"], away_team_logo_pos["y"])
        # self.canvas.SetImage(home_team_logo.convert("RGB"), home_team_logo_pos["x"], home_team_logo_pos["y"])
    # Load the canvas on screen.
    self.canvas = self.matrix.SwapOnVSync(self.canvas)
    # Refresh the Data image.
    self.image = Image.new('RGB', (self.width, self.height))
    self.draw = ImageDraw.Draw(self.image)

    warmup_text = pregame.status
    coords = layout.coords("pregame.warmup_text")
    font = layout.font("pregame.warmup_text")
    warmup_x = center_text_position(warmup_text, coords["x"], font["size"]["width"])
    graphics.DrawText(canvas, font["font"], warmup_x, coords["y"], color, warmup_text)

# def _render_start_time(canvas, layout, colors, pregame):
#     time_text = pregame.start_time
#     coords = layout.coords("pregame.start_time")
#     font = layout.font("pregame.start_time")
#     color = colors.graphics_color("pregame.start_time")
#     time_x = center_text_position(time_text, coords["x"], font["size"]["width"])
#     graphics.DrawText(canvas, font["font"], time_x, coords["y"], color, time_text)


# def _render_warmup(canvas, layout, colors, pregame):
#     warmup_text = pregame.status
#     coords = layout.coords("pregame.warmup_text")
#     font = layout.font("pregame.warmup_text")
#     color = colors.graphics_color("pregame.warmup_text")
#     warmup_x = center_text_position(warmup_text, coords["x"], font["size"]["width"])
#     graphics.DrawText(canvas, font["font"], warmup_x, coords["y"], color, warmup_text)


# def _render_probable_starters(canvas, layout, colors, pregame, probable_starter_pos, pregame_weather):
#     coords = layout.coords("pregame.scrolling_text")
#     font = layout.font("pregame.scrolling_text")
#     color = colors.graphics_color("pregame.scrolling_text")
#     bgcolor = colors.graphics_color("default.background")
#     if pregame_weather and pregame.pregame_weather:
#         pitchers_text = pregame.away_starter + " vs " + pregame.home_starter + " Weather: " + pregame.pregame_weather
#     else :
#         pitchers_text = pregame.away_starter + " vs " + pregame.home_starter
#     return scrollingtext.render_text(
#         canvas, coords["x"], coords["y"], coords["width"], font, color, bgcolor, pitchers_text, probable_starter_pos
#     )
