import cv2
import numpy as np
import pytesseract
import re
import sys
from PIL import Image

TOP_LOW = np.array([215, 215, 215])
TOP_HIGH = np.array([240, 240, 240])

BLUE_LOW = np.array([180, 110, 60])
BLUE_HIGH = np.array([240, 160, 120])

RED_LOW = np.array([30, 15, 170])
RED_HIGH = np.array([80, 80, 220])

TEXT_WHITE_LOW = np.array([200, 200, 200])
TEXT_WHITE_HIGH = np.array([255, 255, 255])

TEXT_BLACK_LOW = np.array([0, 0, 0])
TEXT_BLACK_HIGH = np.array([110, 110, 110])

frames_to_skip = 30

read_link = 'match.mp4'

use_stream = False

def cmdsf(list, loc):
    global frames_to_skip

    if loc + 1 < len(list):
        frames_to_skip = int(list[loc + 1])

def cmdhelp(list,loc):
    print "Usage: python score_detection.py <options>"
    print "Options:"
    print "--skipframes <number>: Sets the amount of frames skipped between reads"
    print "--help: Shows usage and options, then exits"
    print "--use_stream: Use twitch stream instead of file"
    print "--read_from <filename>: Reads from a custom filename. Reads custom url if you are scanning a Twitch stream"

    exit()

def cmdreadfrom(list,loc):
    global read_link

    if loc + 1 < len(list):
        read_link = str(list[loc+1])

def cmdusestream(list,loc):
    global use_stream

    use_stream = True

cmdoptions = {
    "--skipframes": cmdsf,
    "--help" : cmdhelp,
    "--use_stream" : cmdusestream,
    "--read_from" : cmdreadfrom
}

def parseCommandArgs():
    cmdlist = sys.argv[1:len(sys.argv)]

    if len(cmdlist) == 0:
        print "Usage: python score_detection.py <options>"
        print "Use the --help option to get a list of possible options."

        exit()

    for i in range(0,len(cmdlist)):
        if str(cmdlist[i]) in cmdoptions.keys():
            cmdoptions[cmdlist[i]](cmdlist,i)

def getScoreboard(img):
    height, width, channels = img.shape

    return img[int(height * 0.775):height]

def getScoreArea(img, scoreboard):
    _, contours, _ = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    areas = []
    for c in contours:
        areas.append(cv2.contourArea(c))

    sorted_areas = sorted(zip(areas, contours), key=lambda x: x[0], reverse=True)

    largest = sorted_areas[0][1]

    x, y, w, h = cv2.boundingRect(largest)

    return scoreboard[y:y+h, x:x+w]

def getTimeRemaining(scoreboard):
    red_score = cv2.inRange(scoreboard, RED_LOW, RED_HIGH)

    _, red_contours, _ = cv2.findContours(red_score, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    red_areas = []
    for c in red_contours:
        red_areas.append(cv2.contourArea(c))

    sorted_red_areas = sorted(zip(red_areas, red_contours), key=lambda x: x[0], reverse=True)

    red_largest = sorted_red_areas[0][1]

    height, width = scoreboard.shape[:2]
    x, y, w, h = cv2.boundingRect(red_largest)

    cropped = scoreboard[(height-h)/2:height-y, x:x+(2*w)]
    height, width = cropped.shape[:2]

    return cropped[height*0.05:height*0.9, width/2-width/6:width/2+width/6]

parseCommandArgs()
if use_stream:
    print "Twitch Streaming is not supported yet."
    exit()

cap = cv2.VideoCapture(read_link)

match_string = ''

while cap.isOpened():
    # Grab every (frames to skip) frames
    if int(cap.get(cv2.CAP_PROP_POS_FRAMES)) % frames_to_skip != 0:
        cap.read()
        continue

    _, frame = cap.read()

    scoreboard = getScoreboard(frame)

    if match_string == '':
        top_bar = cv2.inRange(scoreboard, TOP_LOW, TOP_HIGH)
        top_bar_cropped = getScoreArea(top_bar, scoreboard)
        long_match_string = pytesseract.image_to_string(Image.fromarray(top_bar_cropped)).strip()
        m = re.search('([a-zA-z]+) ([1-9]+)( of ...?)?', long_match_string)
        if m is not None:
            match_string = m.group(1) + ' ' + m.group(2)

    blue_score = cv2.inRange(scoreboard, BLUE_LOW, BLUE_HIGH)
    red_score = cv2.inRange(scoreboard, RED_LOW, RED_HIGH)

    # kernel = np.ones((5,5),np.float32)/25
    # height, width = top_bar.shape
    # top_bar = cv2.filter2D(top_bar,-1,kernel)[0:height, 0:width/2]

    time_remaining = getTimeRemaining(scoreboard)
    blue_cropped = getScoreArea(blue_score, scoreboard)
    red_cropped = getScoreArea(red_score, scoreboard)

    time_remaining = cv2.inRange(time_remaining, TEXT_BLACK_LOW, TEXT_BLACK_HIGH)
    blue_cropped = cv2.inRange(blue_cropped, TEXT_WHITE_LOW, TEXT_WHITE_HIGH)
    red_cropped = cv2.inRange(red_cropped, TEXT_WHITE_LOW, TEXT_WHITE_HIGH)

    cv2.imshow('Time Remaining', time_remaining)
    cv2.imshow('Blue Score', blue_cropped)
    cv2.imshow('Red Score', red_cropped)

    time_remaining_string = pytesseract.image_to_string(Image.fromarray(time_remaining)).strip()
    blue_score_string = pytesseract.image_to_string(Image.fromarray(blue_cropped)).strip()
    red_score_string = pytesseract.image_to_string(Image.fromarray(red_cropped)).strip()

    if not blue_score_string:
        blue_score_string = '0'
    if not red_score_string:
        red_score_string = '0'

    print '\nFrame: ' + str(int(cap.get(cv2.CAP_PROP_POS_FRAMES)))
    print 'Match: ' + match_string
    print 'Remaining: ' + time_remaining_string
    print 'Blue: ' + blue_score_string
    print 'Red: ' + red_score_string

    if cv2.waitKey(10) == 27:
        break

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        break
