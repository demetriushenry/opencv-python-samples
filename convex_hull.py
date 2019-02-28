import argparse
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


def show_window(name_window, img_mat, ratio=1.8):
    res_w, res_h = get_screen_resolution()

    cv2.namedWindow(name_window, cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow(name_window, int(res_w // ratio), int(res_h // ratio))
    cv2.imshow(name_window, img_mat)


def show_convex_hull(img_path):
    img = cv2.imread(img_path, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(gray, (3, 3))
    ret, thresh = cv2.threshold(blur, 35, 125, cv2.THRESH_BINARY)

    _, contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    hull = []

    for i in range(len(contours)):
        hull.append(cv2.convexHull(contours[i], False))

    result_img = np.zeros((thresh.shape[0], thresh.shape[1], 3), np.uint8)

    for i in range(len(contours)):
        color_contours = (0, 255, 0)
        color = (255, 0, 0)
        
        cv2.drawContours(result_img, contours, i,
                         color_contours, 1, 8, hierarchy)

        cv2.drawContours(result_img, hull, i, color, 1, 8)

    show_window('Convex', result_img)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image', required=True, help='Image source')
    args = parser.parse_args()

    show_convex_hull(args.image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    sys.exit(main())
