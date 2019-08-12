import concurrent.futures
import glob
import os
import random
import time

import cv2
import numpy as np

import pytesseract

os.environ['OMP_THREAD_LIMIT'] = '1'


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


def get_string(args):
    img_path = args[0]
    method = args[1]
    print('method', method)
    img = cv2.imread(img_path)
    kernel = np.ones((1, 1), np.uint8)
    img = change_black_to_white(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    gray = cv2.erode(gray, kernel, iterations=10)
    gray = cv2.dilate(gray, kernel, iterations=10)
    gray = apply_threshold(gray, method)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    tess_config = ("-l eng --oem 1 --psm 6")
    result = pytesseract.image_to_string(gray, config=tess_config)
    result = result.replace('\t', '').replace('\n', ' ')
    return result


def change_black_to_white(frame):
    frame = change_gamma(frame, 0.5)
    black = [0, 0, 0]
    thresh = 75
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
    print('OMP_THREAD_LIMIT:', os.environ['OMP_THREAD_LIMIT'])
    path = "/home/demetrius/Pictures/roi"
    if os.path.isdir(path) == 1:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            image_list = [
                (path, random.randint(1, 7)) for path in glob.glob(path + "/*.jpg")
            ]
            for img_path, out_file in zip(image_list, executor.map(get_string, image_list)):
                print(img_path[0].split("/")[-1], ',', out_file, ', processed')


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print(end - start)
