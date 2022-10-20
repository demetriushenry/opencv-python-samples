import subprocess
import sys

import cv2 as cv
import numpy as np

# Python 2/3 compatibility
PY3 = sys.version_info[0] == 3

if PY3:
    xrange = range


def get_screen_resolution():
    output = subprocess.Popen(
        'xrandr | grep "*" | cut -d" " -f4',
        shell=True,
        stdout=subprocess.PIPE
    ).communicate()[0]

    resolution = output.split()[0].split(b'x')

    return int(resolution[0]), int(resolution[1])


def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs(np.dot(d1, d2) / np.sqrt(np.dot(d1, d1)*np.dot(d2, d2)))


def find_squares(img):
    img = cv.GaussianBlur(img, (5, 5), 0)
    squares = []
    for gray in cv.split(img):
        for thrs in xrange(0, 255, 25):
            if thrs == 0:
                bin = cv.Canny(gray, 50, 200)
                bin = cv.dilate(bin, None)
            else:
                _retval, bin = cv.threshold(gray, thrs, 255, cv.THRESH_BINARY)

            # cv.RETR_TREE for rectangle
            # cv.RETR_LIST for square
            contours, _hierarchy = cv.findContours(
                bin, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv.arcLength(cnt, True)
                cnt = cv.approxPolyDP(cnt, 0.1*cnt_len, True)
                # cv.contourArea(cnt) > [value] according on sizes
                if len(cnt) == 4 and cv.contourArea(cnt) > 13000 \
                        and cv.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max(
                        [angle_cos(
                            cnt[i],
                            cnt[(i+1) % 4],
                            cnt[(i+2) % 4]
                        ) for i in xrange(4)]
                    )
                    if max_cos < 0.1:
                        squares.append(cnt)
    return squares


if __name__ == '__main__':
    img = cv.imread('/images/tv_procel.jpg')
    squares = find_squares(img)
    # for square in squares:
    #     (x, y, w, h) = cv.boundingRect(square)
    #     print(img[y, x])
    cv.drawContours(img, [squares[4]], -1, (255, 0, 255), -1)

    res_w, res_h = get_screen_resolution()

    cv.namedWindow('Squares', cv.WINDOW_NORMAL)
    # cv.resizeWindow('Squares', int(res_w // 1.2), int(res_h // 1.2))
    cv.imshow('Squares', img)

    cv.waitKey(0)
    cv.destroyAllWindows()
