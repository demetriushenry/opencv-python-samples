"""ex. python ocr_img_text.py -i /home/demetrius/Pictures/procel_tag.jpg"""
import argparse
import sys
import re

import cv2
import numpy as np
import pytesseract


def apply_threshold(img, method):
    switcher = {
        1: cv2.threshold(cv2.GaussianBlur(img, (9, 9), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        2: cv2.threshold(cv2.GaussianBlur(img, (7, 7), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        3: cv2.threshold(cv2.GaussianBlur(img, (5, 5), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        4: cv2.threshold(cv2.medianBlur(img, 5), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        5: cv2.threshold(cv2.medianBlur(img, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        6: cv2.adaptiveThreshold(cv2.GaussianBlur(img, (5, 5), 0), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2),
        7: cv2.adaptiveThreshold(cv2.medianBlur(img, 3), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    }
    return switcher.get(method, "Invalid method")


def get_string(img, method):
    kernel = np.ones((1, 1), np.uint8)
    # img = change_black_to_white(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # gray = cv2.bitwise_not(gray)
    gray = cv2.erode(gray, kernel, iterations=10)
    gray = cv2.dilate(gray, kernel, iterations=10)
    gray = apply_threshold(gray, method)
    # gray = cv2.GaussianBlur(gray, (3, 3), 0)
    tess_config = ("-l eng --oem 1 --psm 6")
    return img, gray, pytesseract.image_to_string(gray, config=tess_config)


def change_black_to_white(frame):
    frame = change_gamma(frame, 0.5)
    black = [0, 0, 0]
    thresh = 75
    # lower_black = np.array([0, 0, 0])
    # upper_black = np.array([128, 128, 128])
    lower_black = np.array([black[0] - thresh, black[1] - thresh, black[2] - thresh])
    upper_black = np.array([black[0] + thresh, black[1] + thresh, black[2] + thresh])
    black_mask = cv2.inRange(frame, lower_black, upper_black)
    res = cv2.bitwise_and(frame, frame, mask=black_mask)
    return res


def change_gamma(frame, gamma=1.0):
    invGamma = 1.0 / gamma
    table = np.array([
      ((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)])
    return cv2.LUT(frame.astype(np.uint8), table.astype(np.uint8))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True)
    args = parser.parse_args()

    input_img = args.input
    img = cv2.imread(input_img)

    orig, thresh, text = get_string(img, 6)
    text = text.replace('\t', '').replace('\n', '')
    # numbers = re.findall(r'\d+', text)
    # result = ''.join(numbers)

    print('recognized text:', text)
    # print('found numbers:', numbers)
    # print('result:', result)

    cv2.namedWindow('Original', cv2.WINDOW_KEEPRATIO)
    cv2.imshow('Original', orig)
    cv2.namedWindow('Thresh', cv2.WINDOW_KEEPRATIO)
    cv2.imshow('Thresh', thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    sys.exit(main())
