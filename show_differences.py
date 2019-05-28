import argparse
import subprocess
import sys

import cv2
import imutils
import numpy as np
from skimage.measure import compare_ssim


def get_screen_resolution():
    output = subprocess.Popen(
        'xrandr | grep "\*" | cut -d" " -f4',
        shell=True,
        stdout=subprocess.PIPE
    ).communicate()[0]

    resolution = output.split()[0].split(b'x')

    return int(resolution[0]), int(resolution[1])


def show_differences_1(img_source, img_dest):
    img_s = cv2.imread(img_source)
    img_d = cv2.imread(img_dest)

    gray_s = cv2.cvtColor(img_s, cv2.COLOR_BGR2GRAY)
    gray_d = cv2.cvtColor(img_d, cv2.COLOR_BGR2GRAY)

    (score, diff) = compare_ssim(gray_s, gray_d, full=True)
    diff = (diff * 255).astype('uint8')

    print('SSIM:', score)

    thresh = cv2.threshold(
        diff,
        0,
        255,
        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
    )[1]

    cnts = cv2.findContours(
        thresh.copy(),
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(img_s, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(img_d, (x, y), (x + w, y + h), (0, 0, 255), 2)

    h_images_1 = np.hstack((img_s, img_d))
    h_images_2 = np.hstack((diff, thresh))

    res_w, res_h = get_screen_resolution()

    ratio = 1.8

    # cv2.namedWindow('Original', cv2.WINDOW_KEEPRATIO)
    # cv2.resizeWindow('Original', int(res_w // ratio), int(res_h // ratio))

    # cv2.namedWindow('Modified', cv2.WINDOW_KEEPRATIO)
    # cv2.resizeWindow('Modified', int(res_w // ratio), int(res_h // ratio))

    # cv2.namedWindow('Difference', cv2.WINDOW_KEEPRATIO)
    # cv2.resizeWindow('Difference', int(res_w // ratio), int(res_h // ratio))

    # cv2.namedWindow('Thresh', cv2.WINDOW_KEEPRATIO)
    # cv2.resizeWindow('Thresh', int(res_w // ratio), int(res_h // ratio))

    cv2.namedWindow('Result', cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow('Result', int(res_w // ratio), int(res_h // ratio))

    cv2.namedWindow('Difference', cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow('Difference', int(res_w // ratio), int(res_h // ratio))

    # cv2.imshow('Original', img_s)
    # cv2.imshow('Modified', img_d)
    # cv2.imshow('Difference', diff)
    # cv2.imshow('Thresh', thresh)
    cv2.imshow('Result', h_images_1)
    cv2.imshow('Difference', h_images_2)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def show_differences_2(img_source, img_dest):
    img_s = cv2.imread(img_source)
    img_d = cv2.imread(img_dest)

    diff = cv2.absdiff(img_s, img_d)

    mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    th = 0
    imask = mask > th

    canvas = np.zeros_like(img_d, np.uint8)
    canvas[imask] = img_d[imask]

    res_w, res_h = get_screen_resolution()

    ratio = 1.8

    cv2.namedWindow('Mask', cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow('Mask', int(res_w // ratio), int(res_h // ratio))

    cv2.imshow('Mask', mask)

    cv2.namedWindow('Resultado', cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow('Resultado', int(res_w // ratio), int(res_h // ratio))

    cv2.imshow('Resultado', canvas)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def show_differences_3(img_source, img_dest):
    img_s = cv2.imread(img_source)
    img_d = cv2.imread(img_dest)

    diff = cv2.absdiff(img_s, img_d)

    mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(mask, 127, 255, 0)

    im2, contours, hierarchy = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    cv2.drawContours(img_s, contours, -1, 255, 4)

    res_w, res_h = get_screen_resolution()

    ratio = 1.8

    cv2.namedWindow('Mask', cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow('Mask', int(res_w // ratio), int(res_h // ratio))

    cv2.imshow('Mask', mask)

    cv2.namedWindow('Resultado', cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow('Resultado', int(res_w // ratio), int(res_h // ratio))

    cv2.imshow('Resultado', img_s)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def show_differences_4(img_source, img_dest):
    img_out = cv2.imread(img_source)
    img_s = cv2.cvtColor(img_out, cv2.COLOR_BGR2GRAY)
    img_d = cv2.imread(img_dest, cv2.IMREAD_GRAYSCALE)

    diff = cv2.absdiff(img_s, img_d)

    _, thresh = cv2.threshold(
        diff,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    kernel = np.ones((5, 5), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    kernel = np.ones((6, 6), np.uint8)
    dilate = cv2.dilate(opening, kernel, iterations=1)

    blur = cv2.blur(dilate, (15, 15))

    _, thresh = cv2.threshold(
        blur,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    cnts, _ = cv2.findContours(
        thresh.copy(),
        cv2.RETR_LIST,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # cnt = max(cnts, key=cv2.contourArea)

    # h, w = img_out.shape[:2]
    # mask = np.zeros((h, w), np.uint8)

    # cv2.drawContours(mask, [cnt], -1, 255, 8)
    # res = cv2.bitwise_and(img_out, img_out, mask=mask)

    for cnt in cnts:
        (x, y, w, h) = cv2.boundingRect(cnt)
        cv2.rectangle(img_out, (x, y), (x + w, y + h), (0, 255, 0), 16)

    res_w, res_h = get_screen_resolution()

    ratio = 1.8

    cv2.namedWindow('Thresh', cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow('Thresh', int(res_w // ratio), int(res_h // ratio))

    cv2.imshow('Thresh', thresh)

    cv2.namedWindow('Resultado', cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow('Resultado', int(res_w // ratio), int(res_h // ratio))

    cv2.imshow('Resultado', img_out)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--original', required=True, help='Image source')
    parser.add_argument('-d', '--modified', required=True, help='Image destiny')
    args = parser.parse_args()

    original = args.original
    modified = args.modified

    show_differences_1(original, modified)


if __name__ == "__main__":
    sys.exit(main())
