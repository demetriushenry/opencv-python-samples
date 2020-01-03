import sys

import cv2
import numpy as np


def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs(np.dot(d1, d2) / np.sqrt(np.dot(d1, d1)*np.dot(d2, d2)))


def main():
    img = cv2.imread('images/panel-sheet.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # get threshold
    blur = cv2.GaussianBlur(gray, (9, 9), 15)
    _, threshold = cv2.threshold(
        blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # find contours
    squares = []
    cnts, _ = cv2.findContours(
        threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in cnts:
        cnt_len = cv2.arcLength(cnt, True)
        cnt = cv2.approxPolyDP(cnt, 0.1*cnt_len, True)
        if len(cnt) == 4 and cv2.contourArea(cnt) > 300000 \
                and cv2.isContourConvex(cnt):
            cnt = cnt.reshape(-1, 2)
            max_cos = np.max(
                [angle_cos(
                    cnt[i],
                    cnt[(i+1) % 4],
                    cnt[(i+2) % 4]
                ) for i in range(4)]
            )
            if max_cos < 1.0:
                squares.append(cnt)
        # squares.append(cnt)

    # draw contours
    color = (255, 0, 255)
    cv2.drawContours(img, [squares[0]], 0, color, -1)

    # update threshold
    lower = np.array([255, 0, 255])
    upper = np.array([255, 0, 255])
    mask = cv2.inRange(img, lower, upper)

    cv2.namedWindow('Thresh', cv2.WINDOW_NORMAL)
    cv2.imshow('Thresh', threshold)
    cv2.namedWindow('Mask', cv2.WINDOW_NORMAL)
    cv2.imshow('Mask', mask)
    cv2.namedWindow('Original', cv2.WINDOW_NORMAL)
    cv2.imshow('Original', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    sys.exit(main())
