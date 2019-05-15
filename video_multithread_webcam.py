import time
from datetime import datetime
from threading import Lock, Thread

import cv2
import imutils
import numpy as np
from imutils.video import FPS, WebcamVideoStream


mutex = Lock()


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


def detect(frame, model_face, model_eyes):
    with mutex:
        cascade_face = cv2.CascadeClassifier(model_face)
        cascade_eyes = cv2.CascadeClassifier(model_eyes)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        faces = cascade_face.detectMultiScale(gray, minNeighbors=10)
        for (x, y, w, h) in faces:
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (255, 0, 255),
                2
            )

            face_roi = gray[y:y+h, x:x+w]
            eyes = cascade_eyes.detectMultiScale(face_roi)
            # if len(eyes) == 2:
            for (x2, y2, w2, h2) in eyes:
                eye_center = (x + x2 + w2//2, y + y2 + h2//2)
                radius = int(round((w2 + h2)*0.25))
                frame = cv2.circle(frame, eye_center, radius, 255, 2)

        # frame = cv2.flip(frame, 1)

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
            frame = detect(
                self.frame,
                'data/haarcascade_frontalface_default.xml',
                'data/haarcascade_eye.xml',
            )
            cv2.imshow('Video', frame)
            if cv2.waitKey(1) == ord('q'):
                self.stopped = True


class ObjectDetector:

    def __init__(self, model_face, model_eyes=None, frame=None, det_eyes=True):
        self.model_face = model_face
        self.model_eyes = model_eyes
        self._frame = frame
        self.stopped = False
        self.detect_eyes = det_eyes

    def start(self):
        t = Thread(target=self.detect, args=())
        t.daemon = True
        t.start()
        return self

    def stop(self):
        self.stopped = True

    def detect(self):
        cascade_face = cv2.CascadeClassifier(self.model_face)
        if self.model_eyes:
            cascade_eyes = cv2.CascadeClassifier(self.model_eyes)

        while True:
            if self.stopped:
                return

            gray = cv2.cvtColor(self._frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)

            faces = cascade_face.detectMultiScale(gray, 1.1, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(
                    self._frame,
                    (x, y),
                    (x + w, y + h),
                    (255, 0, 255),
                    2
                )

                if self.model_eyes and self.detect_eyes:
                    face_roi = gray[y:y+h, x:x+w]
                    eyes = cascade_eyes.detectMultiScale(face_roi, 1.1, 1)
                    for (x2, y2, w2, h2) in eyes:
                        cv2.rectangle(
                            self._frame,
                            (x + x2, y + y2),
                            (x + x2 + w2, y + y2 + h2),
                            (255, 0, 0),
                            2
                        )

    def update(self, frame):
        self._frame = frame

    def read(self):
        return self._frame


wbs = WebcamVideoStream(0)
# wbs.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
# wbs.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
# wbs.stream.set(cv2.CAP_PROP_AUTOFOCUS, 0)
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

video_show = VideoShow(wbs.read()).start()
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
