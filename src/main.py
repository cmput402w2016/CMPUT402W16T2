# the minimal main.py program to load the video controller, log controller.
# runs the program adhering to MVC requirements
from src.views.expanded_tk import TkWindowViewer
from src.controllers.videocontroller import VideoController
from src.controllers.logcontroller import LogController
DEBUG = True
#RUN_GUI = DEBUG

PLAY_STATUS = True
PLAY_STRING = "Play" if PLAY_STATUS else "Stop" 

def main():
    global PLAY_STATUS
    maintk = TkWindowViewer()
    maintk.play_stop_string.set(PLAY_STRING)
    # TODO: Do not hardcode this
    vc = VideoController("W:/Troy/Development/CMPUT402W16T2/videos/sample_video_3.mp4")
    lc = LogController()
    
    (frame, count) = vc.runIteration()
 
    maintk.setDisplayImg(frame)
    
    maintk.runMainloop()

if __name__ == "__main__":
    main()
