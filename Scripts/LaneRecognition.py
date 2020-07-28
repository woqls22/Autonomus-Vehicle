import cv2
import numpy as np
import matplotlib.pyplot as plt


# 캐니 에지 디텍션
def Canny(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    canny = cv2.Canny(blur, 50, 200)
    return canny

def InterestRegion(frame, width, height):
    # Width 1280기준
    frame = np.array(frame, dtype=np.uint8)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    lower_white = np.array([110,110,110])
    upper_white = np.array([255,255,255])

    mask_white = cv2.inRange(rgb, lower_white, upper_white)
    res = cv2.bitwise_and(frame, frame, mask = mask_white)

    area = np.array([[(width*0.5,(height*0.4)),(0,(height*0.65)),(0,height), (width,height),(width,(height*0.6))]], np.int32) # Area 지정
    mask = np.zeros_like(frame)
    cv2.fillPoly(mask, area, (0,150,255))
    interestarea = cv2.bitwise_and(res, mask)
    #cv2.imshow('mask',interestarea)
    return interestarea


def Hough_lines(interestregion, rho, theta, threshold, min_line_len, max_line_gap):
    lines = cv2.HoughLinesP(interestregion,rho,theta,threshold,np.array([]),minLineLength=min_line_len, maxLineGap=max_line_gap)
    return lines

def weighted_img(img, initial_img, a=1, b=1., l=0.): # 두 이미지 operlap 하기
    return cv2.addWeighted(initial_img, a, img, b, l)

def draw_lines(frame, lines, color=[0, 0, 255], thickness=2): # 선 그리기
    cv2.line(frame, (lines[0], lines[1]), (lines[2], lines[3]), color, thickness)


def get_representative(frame, lines):  # Representative Line 구하기
    lines = np.squeeze(lines)
    lines = lines.reshape(lines.shape[0] * 2, 2)
    rows, cols = frame.shape[:2]
    output = cv2.fitLine(lines, cv2.DIST_L2, 0, 0.01, 0.01)
    vx, vy, x, y = output[0], output[1], output[2], output[3]
    x1, y1 = int(((frame.shape[0] - 1) - y) / vy * vx + x), frame.shape[0] - 1
    x2, y2 = int(((frame.shape[0] / 2 + 100) - y) / vy * vx + x), int(frame.shape[0] / 2 + 100)

    result = [x1, y1, x2, y2]
    return result

def top_view(frame, width, height):
    #area = np.array([[(width*0.5,(height*0.4)),(0,(height*0.65)),(0,height), (width,height),(width,(height*0.6))]], np.int32) # Area 지정
    #좌상, 좌하, 우상, 우하
    '''
    cv2.circle(frame, (int(width*0.2), int(height*0.6)), 5, (255, 255, 255), -1)
    cv2.circle(frame, (int(width * 0.7), int(height * 0.6)), 5, (255, 255, 255), -1)
    '''
    left_bottom = [0,height]
    right_bottom = [width,height]
    left_top = [int(width*0.2),int(height*0.55)]
    right_top = [int(width*0.7), int(height*0.55)]
    pts1 = np.float32([[left_top,left_bottom,right_top,right_bottom]])
    # 좌표의 이동점
    pts2 = np.float32([[0, 0], [0, 480], [640, 0], [640, 480]])
    # pts1의 좌표에 표시. perspective 변환 후 이동 점 확인.
    M = cv2.getPerspectiveTransform(pts1, pts2)
    dst = cv2.warpPerspective(frame, M, (640, 480))
    cv2.imshow('BirdView',dst)