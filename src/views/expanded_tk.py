from tkFileDialog import askopenfilename

from PIL import Image, ImageTk
from src.controllers.videocontroller import VideoController


try:
    import tkinter as tk 
except ImportError:
    import Tkinter as tk
    
WORLD_COORDINATES = "1200x550"

    
class TkWindowViewer:
    """
    Manages a TKinter window by packing together opencv operations that cleanly handles 
    updating a frame inside the main video window, and updating the built-in log file display.
    Also holds a GUI frame of "remote control" options to select, run, and stop a video file. 
    
    Class variables are used instead of tk's name convention for windows
    for accessibility, permanence, and simplicity. 
    
    Must be called manually in order to write to the log frame
    """
    def __init__(self):
        #initialize root        
        self.root = tk.Tk()
        self.root.geometry(WORLD_COORDINATES)
        self.root.grid_propagate(0)
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        #initialize frames so they can be referenced and packed
        self.video_frame = None #packs nicely into the gui
        self.video_label = None #holds the image
        
        self.log_frame = None
        self.remote_frame = None
        #Flag sent through update to kill video infinite loop
        #set to stop for init
        self.PLAY = 0 
        
        
        self.play_stop_button = None
        #initialize other variables
        self._buildWindow()
        self._buildMenu()
        
        #inintialize a reference to the active video controller
        self.active_vc = None
        
    def runMainloop(self):
        self.root.mainloop()
    
    def runUpdate(self):
        self.root.update()
        return self.PLAY
        
    def runActiveVideo(self):
        self.PLAY = not(self.PLAY)
        self.play_stop_button.configure(text="Play" if self.PLAY else "Stop")
        self.active_vc.runInfinite(self)
    
    def loadVideoFile(self):
        #opens window, selects a file name and configures windows to play it
        filename = askopenfilename()
        self.file_label.configure(text=filename)
        self.active_vc = VideoController(filename)
        self.play_stop_button.configure(text="Play")
        pass
        
    def setDisplayImg(self, imgarray=None):
        #convert img into TkPhoto object
        if imgarray is not None:
            im = Image.fromarray(imgarray)
            imgtk = ImageTk.PhotoImage(image=im)
            #put in display window
            self.video_label.configure(image = imgtk)
            self.video_label.image = imgtk
        else:
            self.video_label.configure(image=None)
            self.video_label.image = None
 
    def setbuttontext(self, text):
        self.play_stop_string.set(text)
        
    def _buildWindow(self):
        self.video_frame = tk.Frame(master=self.root,width=800,height=450,bg="black")
        self.video_frame.grid(row=0,column=0)
        self.video_frame.grid_propagate(0)
        
        self.file_label= tk.Label(master=self.video_frame, width=800,height=1,text="--No file selected--")
        self.file_label.grid(row=0,column=0)
        
        self.video_label = tk.Label(master = self.video_frame, width=800, height=450,bg="grey",image=None)    
        #initialize a reference to an image file. Needs to be updated each time it is changed
        self.video_label.image = None
        self.video_label.grid(row=0,column=1)
         
        self.log_frame = tk.LabelFrame(master=self.root, text="Log", labelanchor=tk.N, width=400, height=550,bg="white")
        self.log_frame.grid(row=0,column=1,rowspan=2)
        self.log_frame.grid_propagate(0)

        self.remote_frame = tk.Frame(master=self.root, width=800,height=100, bg="white")
        self.remote_frame.grid(row=1,column=0)
        self.remote_frame.grid_propagate(0) 
     
        self.play_stop_button = tk.Button(master=self.remote_frame,
                                          command=self.runActiveVideo,
                                          bg="dark grey",
                                          text="--select video file--",
                                          anchor=tk.N,
                                          width=800,height=100)
        self.play_stop_button.grid(row=0,column=1, sticky = tk.E)
         
    def _buildMenu(self):
        filemenu = tk.Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Open...", command=self.loadVideoFile)
        filemenu.add_separator()
        filemenu.add_command(label="Quit", command=self.root.destroy)
        self.menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=self.menubar)