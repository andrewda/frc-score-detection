# FRC Score Detection

## What Is This?

This is a Python program that makes use of the
[`frc-livescore`](https://github.com/andrewda/frc-livescore) package to gather
match information (such as scores, time remaining, match number, etc.) from the
scoreboard on FRC livestreams. This will allow us to get live updates on matches
and allows us to know when a match finishes before the API officially reports
them. It has almost a 100% accuracy in reading scores and remaining time from
images thanks to [Tesseract](https://github.com/tesseract-ocr/tesseract).

For example, take the following scene:

![Example Scene](screenshots/scene1.png)

This image will give us the following data:

```text
Match: Qualification 16
Remaining: 88
Red: 115
Blue: 113
```

[That's pretty good!](https://www.youtube.com/watch?v=JeimE8Wz6e4)

## Running Score Detector

### Installing Dependencies

```bash
pip install -r requirements.txt
```

You will also need to have [Tesseract](https://github.com/tesseract-ocr/tesseract/wiki#installation)
and OpenCV 3 (instructions for
[macOS](http://www.pyimagesearch.com/2016/12/19/install-opencv-3-on-macos-with-homebrew-the-easy-way/),
[Windows](http://docs.opencv.org/3.2.0/d5/de5/tutorial_py_setup_in_windows.html) and
[Linux](http://docs.opencv.org/3.2.0/d7/d9f/tutorial_linux_install.html))
installed.

### Running

To run the program, use the following command:

```bash
$ python score_detection.py
```
