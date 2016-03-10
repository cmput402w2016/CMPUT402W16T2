# the minimal main.py program to load the video controller, log controller.
# runs the program adhering to MVC requirements

import argparse
from views.expanded_tk import TkWindowViewer
from controllers.videocontroller import VideoController
from controllers.logcontroller import LogController

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str, help="path to the video file", required=True)
args = vars(ap.parse_args())

DEBUG = True
#RUN_GUI = DEBUG

PLAY_STATUS = True
PLAY_STRING = "Play" if PLAY_STATUS else "Stop"

def main():
    global PLAY_STATUS
    maintk = TkWindowViewer()
    maintk.play_stop_string.set(PLAY_STRING)
    # TODO: Do not hardcode this
    vc = VideoController(args["video"])
    lc = LogController()

    (frame, count) = vc.runIteration()
    maintk.setDisplayImg(frame)

    maintk.setplay(lambda: vc.runInfinite(maintk))
    maintk.runMainloop()

if __name__ == "__main__":
    main()
