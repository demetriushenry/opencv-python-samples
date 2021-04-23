import argparse
import sys

import cv2
import numpy as np

import pytesseract as ocr
from pytesseract import Output


def view_image(name, frame):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.imshow(name, frame)


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


def find_hsv_mask(frame, lower, upper):
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(frame_hsv, lower, upper)

    ones = np.ones((3, 3), np.uint8)
    # mask = cv2.dilate(mask, ones, iterations=1)
    # mask = cv2.erode(mask, ones, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, ones, iterations=1)
    mask = cv2.medianBlur(mask, 5)

    mask = cv2.bitwise_not(mask)

    result = cv2.bitwise_and(frame, frame, mask=mask)
    result[mask == 0] = ([255, 255, 255])

    return mask, result
    # return mask


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True)
    args = parser.parse_args()

    input_img = args.input
    img = cv2.imread(input_img)

    (lower, upper) = get_img_range_hsv(
        '/home/demetrius/Pictures/roi/modelo_hsv.jpg')

    print(lower)
    print(upper)

    hsv_mask, frame = find_hsv_mask(img.copy(), lower, upper)

    config = ('-l eng --oem 3 --psm 6')
    ocr_text = ocr.image_to_string(hsv_mask, config=config)
    print('result', '>>', ocr_text)
    # d = ocr.image_to_data(hsv_mask, output_type=Output.DICT)
    # for k, v in d.items():
    #     print(k, v)

    view_image('Frame', frame)
    view_image('Mask', hsv_mask)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    sys.exit(main())
