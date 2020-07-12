import cv2
import numpy as np
import matplotlib.pyplot as plt


# 캐니 에지 디텍션
def Canny(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny

#관심 영역
def InterestRegion(frame):
    # Width 1280기준
    height = frame.shape[0]
    area = np.array([[(300,height), (1200,height), (650,250)]]) # Area 지정
    mask = np.zeros_like(frame)
    cv2.fillPoly(mask, area, 255)
    interestarea = cv2.bitwise_and(frame, mask)
    return interestarea

def Hough_lines(interestregion, rho, theta, threshold, min_line_len, max_line_gap):
    lines = cv2.HoughLinesP(interestregion,rho,theta,threshold,np.array([]),minLineLength=min_line_len, maxLineGap=max_line_gap)
    #line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    #draw_lines(line_img, lines)
    return lines

def weighted_img(img, initial_img, a=1, b=1., l=0.): # 두 이미지 operlap 하기
    return cv2.addWeighted(initial_img, a, img, b, l)

def draw_lines(frame, lines, color=[0, 255, 0], thickness=2): # 선 그리기
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(frame, (x1, y1), (x2, y2), color, thickness)