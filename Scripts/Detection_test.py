import cv2
import numpy as np
import matplotlib.pyplot as plt
import LaneRecognition as LR

capture = cv2.VideoCapture("./test_video.mp4")
if(not capture.isOpened()):
    print("Error : Opening Video")

height, width = (int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)))

while True:
    if (capture.get(cv2.CAP_PROP_POS_FRAMES) == capture.get(cv2.CAP_PROP_FRAME_COUNT)):
        capture.open("./test_video.mp4")
    retval, frame = capture.read()
    cv2.imshow('Original Video', frame)
    canny = LR.Canny(frame)
    InterestArea = LR.InterestRegion(canny)
    cv2.imshow('InterestArea', InterestArea)
    line_arr = LR.Hough_lines(InterestArea, 1,1*np.pi/180,30,10,20) #허프변환
    line_arr = np.squeeze(line_arr)
    #gradient 도출
    slope_degree = (np.arctan2(line_arr[:, 1] - line_arr[:, 3], line_arr[:, 0] - line_arr[:, 2]) * 180) / np.pi
    # 수평 기울기 제한
    line_arr = line_arr[np.abs(slope_degree) < 160]
    slope_degree = slope_degree[np.abs(slope_degree) < 160]
    # 수직 기울기 제한
    line_arr = line_arr[np.abs(slope_degree) > 95]
    slope_degree = slope_degree[np.abs(slope_degree) > 95]
    # 필터링된 직선 버리기
    L_lines, R_lines = line_arr[(slope_degree > 0), :], line_arr[(slope_degree < 0), :]
    temp = np.zeros((frame.shape[0], frame.shape[1], 3), dtype=np.uint8)
    L_lines, R_lines = L_lines[:, None], R_lines[:, None]
    # 직선 그리기
    LR.draw_lines(temp, L_lines)
    LR.draw_lines(temp, R_lines)
    result = LR.weighted_img(temp, frame)  # 원본 이미지에 검출된 선 overlap
    cv2.imshow('result', result)  # 결과 이미지 출력


    if cv2.waitKey(33) > 0: break

capture.release()
cv2.destroyAllWindows()