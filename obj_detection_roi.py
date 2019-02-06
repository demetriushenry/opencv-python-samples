import random
import subprocess
import sys

import cv2 as cv
import numpy as np


def get_sub_images_6(original_img_path: str):
    img = cv.imread(original_img_path)

    shape = img.shape
    rows = shape[0]
    columns = shape[1]

    num_col = 3
    num_row = 2
    roi_list = []
    roi_width = columns // 3
    roi_height = rows // 2

    for i in range(num_row):
        for j in range(num_col):
            x = j * roi_width
            y = i * roi_height
            w = roi_width
            h = roi_height
            roi_list.append((x, y, w, h))

    list_imgs = [img[c[1]:c[1]+c[3], c[0]:c[0]+c[2]] for c in roi_list]

    return list_imgs


def get_screen_resolution():
    output = subprocess.Popen(
        'xrandr | grep "\*" | cut -d" " -f4',
        shell=True,
        stdout=subprocess.PIPE
    ).communicate()[0]

    resolution = output.split()[0].split(b'x')

    return int(resolution[0]), int(resolution[1])


def main():
    cc = lambda: random.randint(0, 200)

    obj_cascade = cv.CascadeClassifier('data/lbpcascade_brown_tape.xml')

    img_path = 'images/20190129_114859.jpg'

    list_imgs = get_sub_images_6(img_path)
    result_list = []

    for id, img in enumerate(list_imgs):
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        # detect object
        objs = obj_cascade.detectMultiScale(gray, 1.1, 2)

        # print(len(objs))

        for index, (x, y, w, h) in enumerate(objs):
            color = (cc(), cc(), cc())
            cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 3)

            label = 'gasket - {}'.format(index + 1)

            (label_w, label_h), baseline = cv.getTextSize(
                label,
                cv.FONT_HERSHEY_SIMPLEX,
                1.0,
                2
            )

            cv.rectangle(
                img,
                (x, y - label_h - int(baseline * 1.8)),
                (x + int(label_w), y - int(baseline * 0.4)),
                color,
                cv.FILLED
            )

            cv.putText(
                img,
                label,
                (x+2, y-12),
                cv.FONT_HERSHEY_SIMPLEX,
                1.0,
                (255, 255, 255),
                2
            )

        result_list.append(img)

    # concatenate horizontal images
    horz_imgs_1 = np.hstack((result_list[0], result_list[1], result_list[2]))
    horz_imgs_2 = np.hstack((result_list[3], result_list[4], result_list[5]))

    # concatenate full image
    full_img = np.vstack((horz_imgs_1, horz_imgs_2))

    res_w, res_h = get_screen_resolution()

    cv.namedWindow('Result', cv.WINDOW_KEEPRATIO)
    cv.resizeWindow('Result', int(res_w // 1.2), int(res_h // 1.2))
    cv.imshow('Result', full_img)

    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == "__main__":
    sys.exit(main())
