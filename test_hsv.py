import sys

import cv2
import numpy as np


def get_img_range_hsv(img_hsv_path):
    img_mask = cv2.imread(img_hsv_path)
    img_hsv = cv2.cvtColor(img_mask, cv2.COLOR_BGR2HSV)
    min = [
        int(img_hsv[..., 0].min()),
        int(img_hsv[..., 1].min()),
        int(img_hsv[..., 2].min())
    ]
    max = [
        int(img_hsv[..., 0].max()),
        int(img_hsv[..., 1].max()),
        int(img_hsv[..., 2].max())
    ]
    return (np.array(min), np.array(max))


def main():
    (lower, upper) = get_img_range_hsv('images/imei_box.jpg')
    print(f'LOWER: {lower}\n')
    print(f'UPPER: {upper}')
    print(f'{2 % 4}')


if __name__ == "__main__":
    sys.exit(main())
