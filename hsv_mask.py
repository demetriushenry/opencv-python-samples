import sys

import cv2
import numpy as np


def view_image(name, img):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.imshow(name, img)


def get_img_range_hsv(img_hsv_path):
    img_mask = cv2.imread(img_hsv_path)
    img_hsv = cv2.cvtColor(img_mask, cv2.COLOR_BGR2HSV)
    min = [
        int(img_hsv[..., 0].min()) - 1,
        int(img_hsv[..., 1].min()) - 1,
        int(img_hsv[..., 2].min()) - 1
    ]
    max = [
        int(img_hsv[..., 0].max()) + 15,
        int(img_hsv[..., 1].max()) + 15,
        int(img_hsv[..., 2].max()) + 15
    ]
    return (min, max)


def main():
    img = cv2.imread('/home/demetrius/Pictures/procel_tag.jpg')
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    (r1, r2) = get_img_range_hsv(
        '/home/demetrius/Pictures/procel_range.jpg')

    lower1 = np.array(r1)
    upper2 = np.array(r2)

    mask = cv2.inRange(img_hsv, lower1, upper2)

    ones = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, ones, iterations=2)
    mask = cv2.dilate(mask, ones, iterations=1)

    # img_hsv[mask > 0] = ([255, 255, 255])

    mask = cv2.bitwise_not(mask)

    # new_bgr = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)

    result = cv2.bitwise_and(img, img, mask=mask)

    result[mask == 0] = ([255, 255, 255])

    view_image('Original', img)
    view_image('HSV', img_hsv)
    view_image('Mask', mask)
    view_image('Result', result)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    sys.exit(main())
