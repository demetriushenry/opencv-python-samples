"""ex. python skew_correction.py -i ./images/text_input.png"""
import argparse
import sys
import math

import cv2
import numpy as np


def compute_skew(img):

    # load in grayscale:
    src = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    height, width = src.shape[0:2]

    # invert the colors of our image:
    cv2.bitwise_not(src, src)

    # hough transform:
    minLineLength = width/2.0
    maxLineGap = 20
    lines = cv2.HoughLinesP(src, 1, np.pi/180, 100, minLineLength, maxLineGap)

    # calculate the angle between each line and the horizontal line:
    angle = 0.0
    nb_lines = len(lines)

    for line in lines:
        angle += math.atan2(line[0][3]*1.0 - line[0][1]
                            * 1.0, line[0][2]*1.0 - line[0][0]*1.0)

    angle /= nb_lines*1.0

    return angle * 180.0 / np.pi


def correct_skew(src_img, angle):
    img = src_img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)

    non_zero_pixels = cv2.findNonZero(gray)
    center, _, _ = cv2.minAreaRect(non_zero_pixels)

    (h, w) = img.shape[:2]
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(
        img,
        M,
        (w, h),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE
    )

    return rotated


def correct_skew_2(src_img):
    img = src_img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)

    thresh = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY | cv2.THRESH_OTSU
    )[1]

    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]

    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(
        img,
        M,
        (w, h),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE
    )

    return rotated


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True)
    args = parser.parse_args()

    input_img = args.input
    img = cv2.imread(input_img)
    # angle = compute_skew(img)
    # rotated_img = correct_skew(img, angle)
    rotated_img = correct_skew_2(img)

    cv2.namedWindow('Original', cv2.WINDOW_KEEPRATIO)
    cv2.imshow('Original', img)
    cv2.namedWindow('Rotated', cv2.WINDOW_KEEPRATIO)
    cv2.imshow('Rotated', rotated_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    sys.exit(main())
