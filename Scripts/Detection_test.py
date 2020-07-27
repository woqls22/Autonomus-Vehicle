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
        cv2.imshow('Original Video', frame)
        InterestArea = LR.InterestRegion(frame, width, height)
        canny = LR.Canny(InterestArea)

        cv2.imshow('InterestArea', canny)
        '''
        line_arr = LR.Hough_lines(InterestArea, 1,1*np.pi/180,30,10,20) #허프변환
        line_arr = np.squeeze(line_arr)
        #gradient 도출
        slope_degree = (np.arctan2(line_arr[:, 1] - line_arr[:, 3], line_arr[:, 0] - line_arr[:, 2]) * 180) / np.pi
        # 수평 기울기 제한
        line_arr = line_arr[np.abs(slope_degree) < 170]
        slope_degree = slope_degree[np.abs(slope_degree) < 170]
        # 수직 기울기 제한
        line_arr = line_arr[np.abs(slope_degree) > 95]
        slope_degree = slope_degree[np.abs(slope_degree) > 95]
        # 필터링된 직선 버리기
        L_lines, R_lines = line_arr[(slope_degree > 0), :], line_arr[(slope_degree < 0), :]
        temp = np.zeros((frame.shape[0], frame.shape[1], 3), dtype=np.uint8)
        L_lines, R_lines = L_lines[:, None], R_lines[:, None]
        LeftLine = LR.get_representative(frame, L_lines)
        RightLine = LR.get_representative(frame, R_lines)

        # 직선 그리기
        Lx1,Ly1,Lx2,Ly2 = LeftLine
        Rx1,Ry1,Rx2,Ry2 = RightLine
        Cx = Lx2+Rx2/2
        #print(Cx)
        Cy = Ly2+Ry2/2
        if(Cx<1050 and Cx>900and Lx2<Rx2):
            LR.draw_lines(temp, LeftLine)
            LR.draw_lines(temp, RightLine)
        result = frame
        result = LR.weighted_img(temp, result)  # 원본 이미지에 검출된 선 overlap
        cv2.imshow('result', result)  # 결과 이미지 출력

        '''

        if (cv2.waitKey(70) > 0):
                break

capture.release()
cv2.destroyAllWindows()