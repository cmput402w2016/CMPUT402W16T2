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
        self.file_label = None
        
        #initialize frames so they can be referenced and packed
        self.video_frame = None #packs nicely into the gui
        self.video_label = None #holds the image
        
        self.log_frame = None
        self.remote_frame = None
        #Flag sent through update to kill video infinite loop
        #set to stop for init
        self.PLAY = 0 
        
        self.LOG_TEXT = None
        
        self.play_stop_button = None
        #initialize other variables
        self._buildWindow()
        self._buildMenu()
        
        #inintialize a reference to the active video controller
        self.active_vc = None
        
    def runMainloop(self):
        self.root.mainloop()
    
    def updateLogText(self, text):
        self.log_listbox.insert(tk.END, text)
    
    def runUpdate(self):
        """
        The update that must be called when inside the video controller
        so that the two infinite loops of the video and the tkinterface
        can run concurrently. Also gets the play signal so another button
        press will pause the frame
        """
        self.root.update()
        return self.PLAY
        
    def runActiveVideo(self):
        """
        Linked to the play button which toggles the kill signal
        read by video player on update, updates the button text
        and then runs the infinite loop inside the video
        controller to play the video into the video_frame
        """
        self.PLAY = not(self.PLAY)
        #play_var should be inverse to what the status is
        play_var = "Stop" if self.PLAY else "Play"
        self.play_stop_button.configure(text=play_var)
        self.active_vc.runInfinite(self)
    
    def loadVideoFile(self):
        """
        instantiates a new video controller and consequently log controller
        needs to be separate from runActiveVideo so that the video controller
        is not recreated accidentally
        """
        #opens window, selects a file name and configures windows to play it
        filename = askopenfilename()
        #self.file_label.configure(text=filename)
        self.active_vc = VideoController(filename)
        self.file_label.configure(text=filename)
        self.play_stop_button.configure(text="Play")
        
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
 
        
    def _buildWindow(self):
      
        self.file_label= tk.Label(master=self.root,
                                  text="-----No File Selected-----",
                                  #width=800,
                                  #height=20
                                  )
        self.file_label.grid(row=0,column=0)
        
        
        self.video_frame = tk.Frame(master=self.root,width=800,height=450,bg="black")
        self.video_frame.grid(row=1,column=0)
        self.video_frame.grid_propagate(0)
 
        self.video_label = tk.Label(master = self.video_frame, width=800, height=450,bg="grey",image=None)    
        #initialize a reference to an image file. Needs to be updated each time it is changed
        self.video_label.image = None
        self.video_label.grid(row=0,column=1)
          
        self.remote_frame = tk.Frame(master=self.root, width=800,height=50, bg="white")
        self.remote_frame.grid(row=2,column=0)
        
 
        self.play_stop_button = tk.Button(master=self.remote_frame,
                                          command=self.runActiveVideo,
                                          text="-----",                                        
                                          #bg="dark grey",
                                          #fg="white",
                                          #anchor=tk.N,
                                          #relief=tk.RAISED,
                                          #width=500,
                                          #height=100
                                          )
        self.play_stop_button.grid(row=0,column=0)
      
        self.log_frame = tk.LabelFrame(master=self.root,
                                        text="Log",
                                        labelanchor=tk.N,
                                        width=400, height=550,
                                        bg="white",
                                        relief=tk.SUNKEN)
        self.log_frame.grid(row=0,column=1,rowspan=3)
        self.log_frame.propagate(0)
        
        self.log_scrollbar = tk.Scrollbar(master=self.log_frame)
        self.log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.log_listbox = tk.Listbox(self.log_frame, height=400,width=300)
        self.log_listbox.pack()
        
                
        self.log_listbox.config(yscrollcommand=self.log_scrollbar.set)
        self.log_scrollbar.config(command=self.log_listbox.yview)
        
         
    def _buildMenu(self):
        filemenu = tk.Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Open...", command=self.loadVideoFile)
        filemenu.add_separator()
        filemenu.add_command(label="Quit", command=self.root.destroy)
        self.menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=self.menubar)