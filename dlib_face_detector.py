import cv2

import dlib

detector = dlib.get_frontal_face_detector()
cam = cv2.VideoCapture(0)
color_green = (0, 255, 0)
line_width = 3

while True:
    ret_val, img = cam.read()
    rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # face detection is faster in gray frame
    dets = detector(rgb_image, 0)
    for det in dets:
        cv2.rectangle(img, (det.left(), det.top()),
                      (det.right(), det.bottom()), color_green, line_width)
    cv2.imshow('DLIB Face Detector', img)
    if cv2.waitKey(1) == 27:
        break  # esc to quit

cam.release()
cv2.destroyAllWindows()
