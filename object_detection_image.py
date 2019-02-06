import random
import subprocess
import sys

import cv2 as cv


def get_screen_resolution():
    output = subprocess.Popen(
        'xrandr | grep "\*" | cut -d" " -f4',
        shell=True,
        stdout=subprocess.PIPE
    ).communicate()[0]

    resolution = output.split()[0].split(b'x')

    return int(resolution[0]), int(resolution[1])


def main():
    obj_cascade = cv.CascadeClassifier('data/lbpcascade_brown_tape.xml')
    img_path = '20190122_170439.jpg'

    img = cv.imread(img_path)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    cc = lambda: random.randint(0, 200)

    objs = obj_cascade.detectMultiScale(gray, 1.1, 2)

    for index, (x, y, w, h) in enumerate(objs):
        color = (cc(), cc(), cc())
        cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 3)
        
        label = 'brown tape - {}'.format(index + 1)

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

    res_w, res_h = get_screen_resolution()

    cv.namedWindow('img', cv.WINDOW_KEEPRATIO)
    cv.resizeWindow('img', int(res_w // 1.2), int(res_h // 1.2))
    cv.imshow('img', img)

    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == "__main__":
    sys.exit(main())
