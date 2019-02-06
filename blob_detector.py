import subprocess
import sys

import cv2
import numpy as np


def get_screen_resolution():
    output = subprocess.Popen(
        'xrandr | grep "\*" | cut -d" " -f4',
        shell=True,
        stdout=subprocess.PIPE
    ).communicate()[0]

    resolution = output.split()[0].split(b'x')

    return int(resolution[0]), int(resolution[1])


def main():
    img = cv2.imread('images/20190129_114859.jpg', cv2.IMREAD_GRAYSCALE)

    detector = cv2.SimpleBlobDetector_create()

    keypoints = detector.detect(img)

    img_keypoints = cv2.drawKeypoints(
        img,
        keypoints,
        np.array([]),
        (255, 0, 255),
        cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
    )

    res_w, res_h = get_screen_resolution()

    cv2.namedWindow('Keypoints', cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow('Keypoints', int(res_w // 1.2), int(res_h // 1.2))
    cv2.imshow('Keypoints', img_keypoints)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    sys.exit(main())
