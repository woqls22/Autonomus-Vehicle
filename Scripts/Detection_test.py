import cv2
import numpy as np
import LaneRecognition as LR
import matplotlib.pyplot as plt

FileName = "./track-s.mkv"
capture = cv2.VideoCapture(FileName)
YOLO_FLAG= True
if(not capture.isOpened()):
        print("Error : Opening Video")

if(YOLO_FLAG):
        net = cv2.dnn.readNet("./yolov3-tiny.weights", "./yolov3-tiny.cfg")
        classes = []
        with open("./coco.names", "r") as f:
                classes = [line.strip() for line in f.readlines()]
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        colors = np.random.uniform(0, 255, size=(len(classes), 3))

height, width = (int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)))
retval, frame = capture.read()
i = 0

while True:
        retval, frame = capture.read()
        cv2.imshow('Original Video', frame)
        if(YOLO_FLAG):
                YOLO = frame.copy()
                heights, widths, channel = YOLO.shape
                blob = cv2.dnn.blobFromImage(YOLO, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
                net.setInput(blob)
                outs = net.forward(output_layers)
                class_ids = []
                confidences = []
                boxes = []
                for out in outs:
                        for detection in out:
                                scores = detection[5:]
                                class_id = np.argmax(scores)
                                confidence = scores[class_id]
                                if confidence > 0.7:
                                        # Object detected
                                        center_x = int(detection[0] * widths)
                                        center_y = int(detection[1] * heights)
                                        w = int(detection[2] * widths)
                                        h = int(detection[3] * heights)
                                        # Rectangle coordinates
                                        x = int(center_x - w / 2)
                                        y = int(center_y - h / 2)
                                        boxes.append([x, y, w, h])
                                        confidences.append(float(confidence))
                                        class_ids.append(class_id)
                indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
                font = cv2.FONT_HERSHEY_PLAIN

                for i in range(len(boxes)):
                        if i in indexes:
                                x, y, w, h = boxes[i]
                                label = str(classes[class_ids[i]])
                                color = colors[i]
                                cv2.rectangle(YOLO, (x, y), (x + w, y + h), color, 2)
                                cv2.putText(YOLO, label, (x, y + 30), font, 3, color, 3)


        InterestArea = LR.InterestRegion(frame, width, height)
        canny = LR.Canny(InterestArea)
        #bird View Point
        dst = LR.top_view(frame, width, height)
        src1 = LR.Canny(dst)

        lines = cv2.HoughLinesP(src1, 0.8, np.pi / 180, 100, minLineLength=100, maxLineGap=60)
        cv2.line(dst, (int(width / 2), height), (int(width / 2), int(height / 1.3)), (255, 255, 0), 8)
        direction = "Go Straight"
        if (lines is not None):
                direction = "Go Straight"
                for i in lines:
                        cv2.line(dst, (i[0][0], i[0][1]), (i[0][2], i[0][3]), (0, 0, 255), 2)
                        if (i[0][2] < int(width / 3)):
                                direction = "Turn Right " + str(abs(width / 2 + i[0][2]))
                        elif (i[0][0] > int(width * 2 / 3)):
                                direction = "Turn Left " + str(abs(width / 2 - i[0][0]))

        dst = cv2.putText(dst, '[Driving Info] : ' + direction, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                          (0, 255, 255), 2, cv2.LINE_AA)

        # Origin Frame------------------------
        cv2.circle(frame, (int(width*0.2), int(height*0.55)), 5, (255, 255, 255), -1)
        cv2.circle(frame, (int(width * 0.8), int(height * 0.55)), 5, (255, 255, 255), -1)
        lines = cv2.HoughLinesP(canny, 1.2, np.pi / 180, 100, minLineLength=100, maxLineGap=60)
        cv2.line(frame, (int(width/2),height), (int(width/2),int(height/1.3)), (255, 255, 0), 8)
        if(lines is not None):
                direction = "Go Straight"
                for i in lines:
                        cv2.line(frame, (i[0][0], i[0][1]), (i[0][2], i[0][3]), (0, 0, 255), 2)
                        if(i[0][2]<int(width/4)):
                                direction = "Turn Right " + str(abs(width/2+i[0][2]))
                        elif(i[0][0]>int(width*3/4)):
                                direction = "Turn Left "+ str(abs(width/2-i[0][0]))

        frame = cv2.putText(frame, '[Driving Info] : '+direction,  (50, 50) , cv2.FONT_HERSHEY_SIMPLEX,0.8, (0,255,255), 2, cv2.LINE_AA)
        cv2.imshow("dst", frame)
        cv2.imshow("dst1",dst)
        if(YOLO_FLAG):
                cv2.imshow("YOLO",YOLO)
        if (cv2.waitKey(2) > 0):
                break
        i = i+1
capture.release()
cv2.destroyAllWindows()