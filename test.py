import numpy as np
import cv2

frame = np.zeros((20,20))
cv2.rectangle(frame,(2,2),(2,2),color=2,thickness=3)

for r in frame:
    print(r)

cv2.imshow('',frame)
cv2.waitKey()
cv2.destroyAllWindows()
    
    