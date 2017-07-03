# FRC Score Detection

## What Is This?

This is a Python program that uses OpenCV to read data (such as scores, time
remaining, match number, etc.) from the scoreboard on FRC livestreams. This will
allow us to get live updates on matches and allows us to know when a match finishes
before the API officially reports them. It has almost a 100% accuracy in reading
scores and remaining time from images thanks to [Tesseract](https://github.com/tesseract-ocr/tesseract).

## Running Score Detector

### Installing dependencies

I recommend using conda (either Anaconda or Miniconda) to install the dependencies.
Once you install conda, run the following commands:

```bash
$ conda install opencv
$ conda install numpy
```

### Downloading Sample Data

Before running the score detector, you'll need a match video (in the future, we'll
allow Twitch links). You can download one [here](https://drive.google.com/file/d/0B3rF-u0VGg5oTHYwajlaX1lQQjA/view?usp=sharing).
Rename this video to `match.mp4` and put it in the source directory.

### Running

To run the program, use the following command:

```bash
$ python score_detection.py
```

A few windows should open up containing the data we want to gather. In the future,
these windows will not be shown and only the data text will appear (see the
[TODO](#todo) below)

## TODO

- [x] Find red/blue score locations
- [x] Find time remaining location
- [x] Find match key location
- [x] Parse red/blue score text ([#1](https://github.com/andrewda/frc-score-detection/issues/1))
- [x] Parse time remaining text ([#2](https://github.com/andrewda/frc-score-detection/issues/2))
- [x] Parse match key text ([#3](https://github.com/andrewda/frc-score-detection/issues/3))
- [ ] Read frames from Twitch ([#4](https://github.com/andrewda/frc-score-detection/issues/4))
- [ ] Export conda environment file ([#5](https://github.com/andrewda/frc-score-detection/issues/5))
