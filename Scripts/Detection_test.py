import cv2
import numpy as np
import LaneRecognition as LR
import matplotlib.pyplot as plt

FileName = "./track-s.mkv"
capture = cv2.VideoCapture(FileName)
if(not capture.isOpened()):
    print("Error : Opening Video")

height, width = (int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)))
retval, frame = capture.read()
while True:
        retval, frame = capture.read()
        #cv2.imshow('Original Video', frame)
        InterestArea = LR.InterestRegion(frame, width, height)
        canny = LR.Canny(InterestArea)

        #cv2.imshow('canny', canny)
        lines = cv2.HoughLinesP(canny, 1, np.pi / 180, 100, minLineLength=70, maxLineGap=30)
        cv2.line(frame, (int(width/2),height), (int(width/2),int(height/1.3)), (255, 0, 255), 2)
        direction = "Go Straight"
        if(lines is not None):
                for i in lines:
                        cv2.line(frame, (i[0][0], i[0][1]), (i[0][2], i[0][3]), (0, 0, 255), 2)
                        if(i[0][2]<int(width/4)):
                                direction = "Turn Right"
                                print("Too Left : Turn Right")
                        elif(i[0][0]>int(width*3/4)):
                                direction = "Turn Left"
                                print("Too Right : Turn Left")
        frame = cv2.putText(frame, '[Driving Info] : '+direction,  (50, 50) , cv2.FONT_HERSHEY_SIMPLEX,0.8, (0,255,255), 2, cv2.LINE_AA)
        cv2.imshow("dst", frame)

        if (cv2.waitKey(70) > 0):
                break

capture.release()
cv2.destroyAllWindows()