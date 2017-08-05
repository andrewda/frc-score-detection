import cmdargs
cmdargs.processArgs()
import cv2
import os
import streamlink
from livescore import Livescore

url = 'http://www.twitch.tv/firstinspires1'

# Create new Livescore instance
frc = Livescore()
if not cmdargs.fileread:

    # Create new read from stream
    streams = streamlink.streams(url)
    stream = streams['best'] # Will crash if stream is not live
    fname = 'read.mpg'
    vid_file = open(fname, 'wb')

    # Buffer video
    fd = stream.open()
    for i in range(0, 512):
        new_bytes = fd.read(1024)
        vid_file.write(new_bytes)

    # Close video file
    vid_file.close()

    # Read frame from buffer
    cam = cv2.VideoCapture(fname)
    ret, img = cam.read()

    # Analyse frame for score info
    score_data = frc.read(img)

    # Display score info
    print score_data
    cv2.imshow('Livestream', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Remove video file
    os.remove(vid_file.name)
else:
    cam = cv2.VideoCapture(cmdargs.readfrom)
    while cam.isOpened():
        if int(cam.get(cv2.CAP_PROP_POS_FRAMES)) % cmdargs.frameskipratevalue != 0:
            cam.read()
            continue
        _,img = cam.read()
        score_data = frc.read(img)

        print score_data
    cv2.waitKey(0)
    cv2.destroyAllWindows()
