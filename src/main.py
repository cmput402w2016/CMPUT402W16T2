# the minimal main.py program to load the video controller, log controller.
# runs the program adhering to MVC requirements

import argparse
from views.expanded_tk import TkWindowViewer
from controllers.videocontroller import VideoController
from controllers.logcontroller import LogController
import datetime

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str, help="path to the video file", required=False)
args = vars(ap.parse_args())
RUN_GUI = True
if args["video"] is not None:
    RUN_GUI = False


PLAY_STATUS = True

def main():
    """
    The gui allows instantiation without a video controller. Once the file
    has been loaded, it calls the video controller's infinite loop when the
    gui "play" button has been pressed. The gui allows pausing and also 
    copies the log file into a side window.
    
    The CLI ultimately writes the same log file as the gui but will run the file
    until Ctrl-C is pressed to kill the process. 
    """
    run_gui() if RUN_GUI else run_cli()

def run_gui():
    maintk = TkWindowViewer()            
    maintk.runMainloop()

def run_cli():
    vc = VideoController(args["video"])
    vc.runInfinite()
    pass

if __name__ == "__main__":
    main()
