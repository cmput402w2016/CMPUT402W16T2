import imutils
import cv2

MIN_AREA = 500

class Frame():
    def __init__(self, img, background_subtractor):
        image = imutils.resize(img, width=500)
        self.image = img
        self.subtracted = background_subtractor.apply(image)
        
    def countVehicles(self):
        count = 0
        contours = self._getContours()
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > MIN_AREA:
                count += 1
    
    def drawCountVehicles(self):
        count = 0
        contours = self._getContours()
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > MIN_AREA:
                (x, y, w, h) = cv2.boundingRect(cnt)
                cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                count += 1
        cv2.putText(self.image,"Count: %d" % count,(10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),2)   
        return (self.image, count)
    
    def _getContours(self):
        # This is an alternative way. Simply just use BackgroundSubtractor.
        thresh = cv2.blur(self.subtracted,(11,11)) # blur the frame. this gives better result
        (contours, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)

        return contours