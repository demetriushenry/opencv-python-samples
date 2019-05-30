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


def show_window(window_name: str, img_mat, ratio=1.8):
    res_w, res_h = get_screen_resolution()

    cv2.namedWindow(window_name, cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow(window_name, int(res_w // ratio), int(res_h // ratio))

    cv2.imshow(window_name, img_mat)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def matching_all_objects(img_source, img_template):
    img_rgb = cv2.imread(img_source)
    template = cv2.imread(img_template)

    w, h = template.shape[:-1]

    method = cv2.TM_CCOEFF_NORMED

    res = cv2.matchTemplate(img_rgb, template, method)

    threshold = 0.8

    loc = np.where(res >= threshold)
    print(loc[::-1])

    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), 255, 4)

    return img_rgb


def matching_object(img_source, img_template):
    img_rgb = cv2.imread(img_source)
    template = cv2.imread(img_template)

    w, h = template.shape[:-1]

    method = cv2.TM_CCOEFF_NORMED

    res = cv2.matchTemplate(img_rgb, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    cv2.rectangle(img_rgb, top_left, bottom_right, 255, 4)

    return img_rgb


def matching_object_2(img_source, img_template):
    method = cv2.TM_SQDIFF_NORMED

    small_image = cv2.imread(img_source)
    large_image = cv2.imread(img_template)

    result = cv2.matchTemplate(small_image, large_image, method)

    mn, _, mnLoc, _ = cv2.minMaxLoc(result)

    MPx, MPy = mnLoc

    trows, tcols = small_image.shape[:2]

    cv2.rectangle(
        large_image,
        (MPx, MPy),
        (MPx+tcols, MPy+trows),
        (0, 0, 255),
        2
    )

    return large_image


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', required=True, help='Image source')
    parser.add_argument('-t', '--template', required=True,
                        help='Image template')
    args = parser.parse_args()

    source_path = args.source
    template_path = args.template

    result = matching_object_2(source_path, template_path)

    show_window('Output', result)


if __name__ == "__main__":
    sys.exit(main())
