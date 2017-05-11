import cv2
import numpy as np

TOP_LOW = np.array([215, 215, 215])
TOP_HIGH = np.array([240, 240, 240])

BLUE_LOW = np.array([180, 110, 60])
BLUE_HIGH = np.array([240, 160, 120])

RED_LOW = np.array([30, 15, 170])
RED_HIGH = np.array([80, 80, 220])

def getScoreboard(img):
    height, width, channels = img.shape

    return img[int(height * 0.775):height]

def getScoreArea(img, scoreboard):
    contours, _ = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    areas = []
    for c in contours:
        areas.append(cv2.contourArea(c))

    sorted_areas = sorted(zip(areas, contours), key=lambda x: x[0], reverse=True)

    largest = sorted_areas[0][1]

    x, y, w, h = cv2.boundingRect(largest)

    return scoreboard[y:y+h, x:x+w]

def getTimeRemaining(scoreboard):
    red_score = cv2.inRange(scoreboard, RED_LOW, RED_HIGH)

    red_contours, _ = cv2.findContours(red_score, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    red_areas = []
    for c in red_contours:
        red_areas.append(cv2.contourArea(c))

    sorted_red_areas = sorted(zip(red_areas, red_contours), key=lambda x: x[0], reverse=True)

    red_largest = sorted_red_areas[0][1]

    height, width, channels = scoreboard.shape
    x, y, w, h = cv2.boundingRect(red_largest)

    return scoreboard[(height-h)/2:height-y, x:x+(2*w)]


cap = cv2.VideoCapture('match.mp4')

pos_frame = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
while cap.isOpened():
    flag, frame = cap.read()

    scoreboard = getScoreboard(frame)

    top_bar = cv2.inRange(scoreboard, TOP_LOW, TOP_HIGH)
    blue_score = cv2.inRange(scoreboard, BLUE_LOW, BLUE_HIGH)
    red_score = cv2.inRange(scoreboard, RED_LOW, RED_HIGH)

    kernel = np.ones((5,5),np.float32)/25
    height, width = top_bar.shape
    top_bar = cv2.filter2D(top_bar,-1,kernel)[0:height, 0:width/2]

    cv2.imshow('Time Remaining', getTimeRemaining(scoreboard))
    cv2.imshow('Match', getScoreArea(top_bar, scoreboard))
    cv2.imshow('Blue Score', getScoreArea(blue_score, scoreboard))
    cv2.imshow('Red Score', getScoreArea(red_score, scoreboard))

    pos_frame = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)

    if cv2.waitKey(10) == 27:
        break

    if cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES) == cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT):
        break
