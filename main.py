import sys

if sys.version_info <= (3, 5):
    print("Error: Please run with python3")
    sys.exit(1)

import logging
import os
import threading
import time

from PIL import Image

import debug
from data import Data
from data.config import Config
from renderers.main import MainRenderer
from utils import args, led_matrix_options
from version import SCRIPT_NAME, SCRIPT_VERSION

try:
    from rgbmatrix import RGBMatrix, __version__

    emulated = False
except ImportError:
    from RGBMatrixEmulator import RGBMatrix, version

    emulated = True

def main(matrix, config_base):

    # Read scoreboard options from config.json if it exists
    config = Config(config_base, matrix.width, matrix.height)
    logger = logging.getLogger("nflled")
    if config.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARNING)

    # Print some basic info on startup
    debug.info("%s - v%s (%sx%s)", SCRIPT_NAME, SCRIPT_VERSION, matrix.width, matrix.height)

    if emulated:
        debug.log("rgbmatrix not installed, falling back to emulator!")
        debug.log("Using RGBMatrixEmulator version %s", version.__version__)
    else:
        debug.log("Using rgbmatrix version %s", __version__)

    data = Data(config)

    # create render thread
    render = threading.Thread(target=__render_main, args=[matrix, data], name="render_thread", daemon=True)
    time.sleep(1)
    render.start()

    __refresh_games(render, data)

def __refresh_games(render_thread, data):
    debug.log("Refreshing game info from main.py")

    starttime = time.time()

    while render_thread.is_alive():
        time.sleep(0.5)
        data.refresh_schedule()

        rotate = data.should_rotate_to_next_game()
        if data.schedule.games_live() and not rotate:
            data.refresh_game()

        endtime = time.time()
        time_delta = endtime - starttime
        rotate_rate = data.config.rotate_rate_for_status(data.current_game.status())

        if time_delta >= rotate_rate and data.scrolling_finished:
            starttime = time.time()
            if rotate:
                data.advance_to_next_game()


def __render_main(matrix, data):
    MainRenderer(matrix, data).render()


if __name__ == "__main__":
    # Check for led configuration arguments
    command_line_args = args()
    matrixOptions = led_matrix_options(command_line_args)

    # Initialize the matrix
    matrix = RGBMatrix(options=matrixOptions)
    try:
        config, _ = os.path.splitext(command_line_args.config)
        main(matrix, config)
    except:
        debug.exception("Untrapped error in main!")
        sys.exit(1)
    finally:
        matrix.Clear()