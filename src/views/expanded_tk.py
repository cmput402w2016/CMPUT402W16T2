try:
    import tkinter as tk 
except ImportError:
    import Tkinter as tk
    
from PIL import Image, ImageTk

WORLD_COORDINATES = "1200x550"
LEFT_FRAME_WIDTH = 480
BUTTON_PADDING = 20
LABEL_FRAME_PADDING = 5
    
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
        self.video_frame = None
        self.log_frame = None
        self.remote_frame = None
        self.play_stop_string = tk.StringVar()
        #initialize other variables
        self._buildWindow()
        self._buildMenu()
        
    def runMainloop(self):
        self.root.mainloop()
    
    def runUpdate(self):
        self.root.update()    
        
    def setDisplayImg(self, imgarray=None):
        #convert img into TkPhoto object
        if imgarray is not None:
            im = Image.fromarray(imgarray)
            imgtk = ImageTk.PhotoImage(image=im)
            #put in display window
            self.video_frame.configure(image = imgtk)
            self.video_frame.image = imgtk
        else:
            self.video_frame.configure(image=None)
            self.video_frame.image = None
 
    def setplay(self,func):
        self.open_file_button.configure(command=func)
 
        
    def _buildWindow(self):
        self.video_frame = tk.Label(master = self.root, text="Video Feed", width=800, height=450,bg="grey",image=None)
        self.video_frame.grid_propagate(0)
        #initialize a reference to an image file. Needs to be updated each time it is changed
        self.video_frame.image = None
        
        self.log_frame = tk.LabelFrame(master=self.root, text="Log", labelanchor=tk.N, width=400, height=550,bg="white")
        self.log_frame.grid_propagate(0)
        self.remote_frame = tk.Frame(master=self.root, width=800,height=100, bg="white")
        self.remote_frame.grid_propagate(0)
        self.open_file_button = tk.Button(master=self.remote_frame, textvariable=self.play_stop_string, width=50,height=15)
        self.open_file_button.grid(row=0,column=1, sticky=tk.NE)
        
        self.video_frame.grid(row=0,column=0)
        
        self.remote_frame.grid(row=1,column=0)
        self.log_frame.grid(row=0,column=1,rowspan=2)
    
        
    def _buildMenu(self):
        filemenu = tk.Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Quit", command=self.root.destroy)
        self.menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=self.menubar)