import time

import cv2
import imutils
import numpy as np
from imutils.video import FPS, FileVideoStream


fvs = FileVideoStream(0)
fvs.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
fvs.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
fvs.stream.set(cv2.CAP_PROP_FPS, 60)
fvs.thread.daemon = True
fvs.start()
time.sleep(1.0)
fps = FPS().start()

while fvs.more():
    frame = fvs.read()
    frame = imutils.resize(frame, height=540)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = np.dstack([frame, frame, frame])

    cv2.putText(
        frame,
        "Queue size: {}".format(fvs.Q.qsize()),
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )

    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break
    fps.update()

fps.stop()
print('Elapsed time: {:.2f}'.format(fps.elapsed()))
print('Approx. FPS: {:.2f}'.format(fps.fps()))

cv2.destroyAllWindows()
fvs.stop()
