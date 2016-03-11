import numpy as np
import cv2
import Tkinter as tk
from PIL import Image, ImageTk

frame = np.zeros((200,200))
cv2.rectangle(frame,(50,50),(150,150),color=100,thickness=3)

root = tk.Tk()
label = tk.Label(master=root, image=None)

label.pack()

im = Image.fromarray(frame)
imtk = ImageTk.PhotoImage(image=im)
label.configure(image=imtk)
label.image = imtk

root.mainloop()

    