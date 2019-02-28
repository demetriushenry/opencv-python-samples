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


def detect_by_range(img_path: str, img_template: str):
    img = cv2.imread(img_path)

    # range color from target obj (lower, upper)
    boundary = get_img_range(img_template)

    lower = np.array(boundary[0])
    upper = np.array(boundary[1])

    mask = cv2.inRange(img, lower, upper)
    output = cv2.bitwise_and(img, img, mask=mask)

    # cv2.imshow('Range Detect', np.hstack([img, output]))
    cv2.imshow('Original', img)
    cv2.imshow('Output', output)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def detect_by_range_2(img_path: str, img_template: str):
    img = cv2.imread(img_path)

    kernel = np.ones((5, 5), np.uint8)

    # range color from target obj (lower, upper)
    boundary = get_img_range(img_template)

    lower = np.array(boundary[0])
    upper = np.array(boundary[1])

    mask = cv2.inRange(img, lower, upper)

    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    cv2.imshow('Mask', opening)

    img = get_rectangles(cv2.cvtColor(opening, cv2.COLOR_GRAY2BGR), img)

    # x, y, w, h = cv2.boundingRect(opening)

    # cv2.rectangle(img, (x, y), (x+w, y + h), (0, 255, 0), 3)
    # cv2.circle(img, (x+w//2, y+h//2), 5, (0, 0, 255), -1)

    res_w, res_h = get_screen_resolution()

    ratio = 1.8

    cv2.namedWindow('Range Detect 2', cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow('Range Detect 2', int(
        res_w // ratio), int(res_h // ratio))

    cv2.imshow('Range Detect 2', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def get_img_range(img_path: str):
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


def get_rectangles(img_mat, img_dest):
    # img = cv2.imread(img_path)

    gray = cv2.cvtColor(img_mat, cv2.COLOR_BGR2GRAY)

    kernel = np.ones((4, 4), np.uint8)
    dilate = cv2.dilate(gray, kernel, iterations=1)
    blur = cv2.GaussianBlur(dilate, (5, 5), 0)

    threshold = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)

    countours, _ = cv2.findContours(
        threshold,
        cv2.RETR_LIST,
        cv2.CHAIN_APPROX_SIMPLE
    )

    coords = []

    for ct in countours:
        approx = cv2.approxPolyDP(
            ct,
            0.07 * cv2.arcLength(ct, True),
            True
        )

        if len(approx) == 4:
            coords.append([ct])
            (x, y, w, h) = cv2.boundingRect(approx)
            
            diff = w / float(h)

            if 0.95 <= diff <= 1.05: type_rect = 'square'
            elif 5 >= diff >= 3: type_rect = 'obround'
            else: type_rect = 'rectangle'

            if type_rect != 'obround':
                cv2.rectangle(img_dest, (x, y), (x+w, y+h), (0, 0, 255), 1)
                # cv2.drawContours(img_dest, [ct], 0, (0, 0, 255), 1)

            # else:
            #     cv2.drawContours(img_dest, [ct], 0, (0, 0, 255), 1)

    return img_dest


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument('-i', '--image', help='image path')
    parse.add_argument('-t', '--template', help='image template')
    args = parse.parse_args()

    detect_by_range_2(args.image, args.template)


if __name__ == "__main__":
    sys.exit(main())
