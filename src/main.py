# the minimal main.py program to load the video controller, log controller.
# runs the program adhering to MVC requirements

import argparse
from views.expanded_tk import TkWindowViewer
from controllers.videocontroller import VideoController
from controllers.logcontroller import LogController
import datetime

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str, help="path to the video file", required=True)
args = vars(ap.parse_args())
RUN_GUI = True
#===============================================================================
# if args["video"] is not None:
#     vc = VideoController(args["video"])
#     RUN_GUI = False
#===============================================================================

PLAY_STATUS = True

def main():
    run_gui() if RUN_GUI else run_cli()

def run_gui():
    maintk = TkWindowViewer()
    #maintk.setbuttontext(PLAY_STRING())
            
    maintk.runMainloop()

def run_cli():
    pass


if __name__ == "__main__":
    main()
