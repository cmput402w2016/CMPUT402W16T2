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
ap.add_argument("-w", "--world", type=str, help="angle1;angle2=from;to , angle3;angle4...", required = True)

args = vars(ap.parse_args())

world = {}
worldargs = args["world"].split(",")
for data in worldargs:
    angles,coords = data.split("=")
    world[str(tuple(angles.split(';')))] = str(tuple(coords.split(';')))
    

RUN_GUI = True
if args["video"] is not None:
    RUN_GUI = False

def main():
    """
    The CLI ultimately writes the same log file as the gui and sends the same posts to
    team 1's server, but will run faster, and use less memory as the entire gui interface
    is circumvented
    
    EDIT: As of sprint 3 the GUI has been deprecated. A debug mode has been implemented
    that allows frame by frame images to display which will show the keypoints and trajectories.
     
    """
    run_cli()

def run_cli():
    vc = VideoController(args["video"], world)
    vc.runInfinite()
    pass

if __name__ == "__main__":
    main()
