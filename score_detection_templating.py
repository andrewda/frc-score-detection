import cv2
import numpy as np
import pytesseract
import re
import sys
import imutils
from PIL import Image

template_scoreboard = cv2.imread('templates/scoreboard.png', 0)
template_scores = cv2.imread('templates/scores.png', 0)
template_time = cv2.imread('templates/time_remaining.png', 0)
template_top = cv2.imread('templates/top_bar.png', 0)

TEXT_WHITE_LOW = np.array([200, 200, 200])
TEXT_WHITE_HIGH = np.array([255, 255, 255])

TEXT_BLACK_LOW = np.array([0, 0, 0])
TEXT_BLACK_HIGH = np.array([105, 105, 135])

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

def matchTemplate(img, template):
    res = cv2.matchTemplate(cv2.cvtColor(img, cv2.COLOR_RGB2GRAY), template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc
    bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])

    return top_left, bottom_right

def getScoreboard(img):
    global template_scoreboard
    template = imutils.resize(template_scoreboard, width=int(template_scoreboard.shape[1]/1280.0*img.shape[1]))
    top_left, bottom_right = matchTemplate(img, template)

    return img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

def getTopBar(img):
    global template_top
    template = imutils.resize(template_top, width=int(template_top.shape[1]/1280.0*img.shape[1]))
    top_left, bottom_right = matchTemplate(img, template)

    return img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

def getTimeArea(img):
    global template_time
    template = imutils.resize(template_time, width=int(template_time.shape[1]/1280.0*img.shape[1]))
    top_left, bottom_right = matchTemplate(img, template)

    located = img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    h, w = located.shape[:2]

    return located[h*0.16:h*0.84, w*0.42:w*0.58]

def getScoreArea(img):
    global template_scores
    template = imutils.resize(template_scores, width=int(template_scores.shape[1]/1280.0*img.shape[1]))
    top_left, bottom_right = matchTemplate(img, template)

    return img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

def getRedScoreArea(img):
    score_area = getScoreArea(img)
    return score_area[:, 0:score_area.shape[1]/2]

def getBlueScoreArea(img):
    score_area = getScoreArea(img)
    return score_area[:, score_area.shape[1]/2:score_area.shape[1]]

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
        top_bar = getTopBar(scoreboard)
        long_match_string = pytesseract.image_to_string(Image.fromarray(top_bar)).strip()
        m = re.search('([a-zA-z]+) ([1-9]+)( of ...?)?', long_match_string)
        if m is not None:
            match_string = m.group(1) + ' ' + m.group(2)

    time_remaining = getTimeArea(scoreboard)
    red_cropped = getRedScoreArea(scoreboard)
    blue_cropped = getBlueScoreArea(scoreboard)

    time_remaining = cv2.inRange(time_remaining, TEXT_BLACK_LOW, TEXT_BLACK_HIGH)
    blue_cropped = cv2.inRange(blue_cropped, TEXT_WHITE_LOW, TEXT_WHITE_HIGH)
    red_cropped = cv2.inRange(red_cropped, TEXT_WHITE_LOW, TEXT_WHITE_HIGH)

    cv2.imshow('Time Remaining', time_remaining)
    cv2.imshow('Blue Score', blue_cropped)
    cv2.imshow('Red Score', red_cropped)

    time_remaining_string = pytesseract.image_to_string(Image.fromarray(time_remaining), config='--psm 8 digits').strip()
    blue_score_string = pytesseract.image_to_string(Image.fromarray(blue_cropped), config='--psm 8 digits').strip()
    red_score_string = pytesseract.image_to_string(Image.fromarray(red_cropped), config='--psm 8 digits').strip()

    print '\nFrame: ' + str(int(cap.get(cv2.CAP_PROP_POS_FRAMES)))
    print 'Match: ' + match_string
    print 'Remaining: ' + time_remaining_string
    print 'Blue: ' + blue_score_string
    print 'Red: ' + red_score_string

    if cv2.waitKey(10) == 27:
        break

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        break
