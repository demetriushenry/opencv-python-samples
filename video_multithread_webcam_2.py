import time
from datetime import datetime
from queue import Queue
from threading import Thread

import cv2
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
            if self.frame is not None:
                cv2.imshow('Video', self.frame)
                self.frame = None
            if cv2.waitKey(1) == ord('q'):
                self.stopped = True


class ObjectDetector:

    def __init__(self, model_face, model_eyes=None, frame=None, det_eyes=True):
        self.model_face = model_face
        self.model_eyes = model_eyes
        self._frame = frame
        self.q = Queue(maxsize=128)
        self.stopped = False
        self.detect_eyes = det_eyes
        self.change_frame = True

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

            if not self.q.full():
                self.change_frame = False

                gray = cv2.cvtColor(self._frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.equalizeHist(gray)

                faces = cascade_face.detectMultiScale(gray)
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
                        eyes = cascade_eyes.detectMultiScale(face_roi)
                        for (x2, y2, w2, h2) in eyes:
                            cv2.rectangle(
                                self._frame,
                                (x + x2, y + y2),
                                (x + x2 + w2, y + y2 + h2),
                                (255, 0, 0),
                                2
                            )

                if len(faces) > 0:
                    self.q.put(self._frame)
                    self.change_frame = True
            else:
                time.sleep(0.5)

            # cv2.imshow('Video', self._frame)
            # if cv2.waitKey(1) == ord('q'):
            #     self.stopped = True

    def update(self, frame):
        self._frame = frame

    def read(self):
        return self.q.get()

    def more(self):
        tries = 0
        while self.q.qsize() == 0 and not self.stopped and tries < 5:
            time.sleep(0.1)
            tries += 1
        return self.q.qsize() > 0

    def running(self):
        return self.more() or not self.stopped


wbs = WebcamVideoStream(0)
# wbs.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
# wbs.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
# wbs.stream.set(cv2.CAP_PROP_AUTOFOCUS, 0)
# wbs.stream.set(cv2.CAP_PROP_FOCUS, 0)
# wbs.stream.set(cv2.CAP_PROP_FPS, 60)
wbs.start()
time.sleep(1.0)
fps = FPS().start()

face_detector = ObjectDetector(
    'data/haarcascade_frontalface_default.xml',
    'data/haarcascade_eye.xml',
    wbs.read()
).start()

video_show = VideoShow(wbs.read()).start()
cps = CountFrame().start()

while face_detector.more() and not video_show.stopped:
    frame = wbs.read()
    # frame = put_iteractions_counting(frame, cps.count_frame())

    face_detector.update(frame)

    video_show.frame = face_detector.read()
    cps.increment()
    fps.update()

fps.stop()
print(cps.count_frame())
print('Elapsed time: {:.2f}'.format(fps.elapsed()))
print('Approx. FPS: {:.2f}'.format(fps.fps()))

cv2.destroyAllWindows()
wbs.stop()
