import sys

import cv2
import numpy as np


def get_img_range_bgr(img_path):
    img = cv2.imread(img_path)

    shape = img.shape
    rows = shape[0]
    columns = shape[1]
    size_list = []

    for i in range(rows):
        for j in range(columns):
            b, g, r = img[i, j]
            size_list.append((b, g, r))

    size_list.sort()

    id_1 = int(len(size_list) * 0.1)
    id_2 = int(len(size_list) * 0.9)

    return (list(size_list[id_1]), list(size_list[id_2]))


def get_img_range_hsv(img_path):
    img = cv2.imread(img_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    shape = hsv.shape
    rows = shape[0]
    columns = shape[1]
    size_list = []

    for i in range(rows):
        for j in range(columns):
            h, s, v = hsv[i, j]
            size_list.append((h, s, v))

    size_list.sort()

    id_1 = int(len(size_list) * 0.1)
    id_2 = int(len(size_list) * 0.9)

    return (list(size_list[id_1]), list(size_list[id_2]))


def main():
    img = cv2.imread('/home/demetrius/Pictures/procel_tag.jpg')
    # Converting the color space from BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    boundary = get_img_range_bgr('/home/demetrius/Pictures/blue_procel.jpg')
    lower_color = np.array(boundary[0])
    upper_color = np.array(boundary[1])

    mask = cv2.inRange(img, lower_color, upper_color)

    # Generating the final output
    res1 = cv2.bitwise_and(img, img, mask=mask)
    # res2 = cv2.bitwise_and(img, img, mask=mask)

    cv2.namedWindow('BGR Color', cv2.WINDOW_KEEPRATIO)
    cv2.imshow('BGR Color', img)
    cv2.namedWindow('Mask not', cv2.WINDOW_KEEPRATIO)
    cv2.imshow('Mask not', res1)
    # cv2.namedWindow('Mask and', cv2.WINDOW_KEEPRATIO)
    # cv2.imshow('Mask and', res2)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    sys.exit(main())
