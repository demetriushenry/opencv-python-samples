import time
from datetime import datetime
from threading import Thread

import cv2
import imutils
import numpy as np
from imutils.video import FPS, WebcamVideoStream


def put_iteractions_counting(frame, iterations):
    cv2.putText(
        frame,
        '{:.0f} iterations/sec'.format(iterations),
        (10, 450),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (255, 255, 255)
    )
    return frame


class CountFrame:

    def __init__(self):
        self._start_time = None
        self._count = 0

    def start(self):
        self._start_time = datetime.now()
        return self

    def increment(self):
        self._count += 1

    def count_frame(self):
        elapsed_time = (datetime.now() - self._start_time).total_seconds()
        return self._count / elapsed_time


class VideoShow:

    def __init__(self, frame=None):
        self.frame = frame
        self.stopped = False

    def start(self):
        t = Thread(target=self.show, args=())
        t.daemon = True
        t.start()
        return self

    def stop(self):
        self.stopped = True

    def show(self):
        while not self.stopped:
            cv2.imshow('Video', self.frame)
            if cv2.waitKey(1) == ord('q'):
                self.stopped = True


wbs = WebcamVideoStream(0)
wbs.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
wbs.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
wbs.stream.set(cv2.CAP_PROP_AUTOFOCUS, 0)
# wbs.stream.set(cv2.CAP_PROP_FOCUS, 0)
# wbs.stream.set(cv2.CAP_PROP_FPS, 60)
wbs.start()
time.sleep(1.0)
fps = FPS().start()

# while True:
#     frame = wbs.read()
#     frame = imutils.resize(frame, height=540)
#     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     frame = np.dstack([frame, frame, frame])

#     cv2.imshow('Frame', frame)
#     if cv2.waitKey(1) == ord('q'):
#         break
#     fps.update()

video_show = VideoShow(wbs.read())
video_show.start()
cps = CountFrame().start()

while not video_show.stopped:
    frame = wbs.read()
    # frame = imutils.resize(frame, height=540)
    # frame = cv2.cvtColor(frame, cvq2.COLOR_BGR2GRAY)
    # frame = np.dstack([frame, frame, frame])
    # frame = put_iteractions_counting(frame, cps.count_frame())
    video_show.frame = frame
    cps.increment()
    fps.update()

fps.stop()
print(cps.count_frame())
print('Elapsed time: {:.2f}'.format(fps.elapsed()))
print('Approx. FPS: {:.2f}'.format(fps.fps()))

cv2.destroyAllWindows()
wbs.stop()
