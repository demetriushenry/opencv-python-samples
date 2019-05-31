import argparse
import glob
import subprocess
import sys

import cv2
import imutils
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

    w, h = img_rgb.shape[:-1]

    method = cv2.TM_CCOEFF_NORMED

    res = cv2.matchTemplate(img_rgb, template, method)

    threshold = 0.8

    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):
        print(pt)
        cv2.rectangle(template, pt, (pt[0] + w, pt[1] + h), 255, 4)

    return template


def matching_object(img_source, img_template):
    img_rgb = cv2.imread(img_source)
    template = cv2.imread(img_template)

    w, h = img_rgb.shape[:-1]

    method = cv2.TM_CCOEFF_NORMED

    res = cv2.matchTemplate(img_rgb, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    cv2.rectangle(template, top_left, bottom_right, 255, 4)

    return template


def matching_object_2(img_source, img_template):
    method = cv2.TM_SQDIFF_NORMED

    small_image = cv2.imread(img_source)
    large_image = cv2.imread(img_template)

    result = cv2.matchTemplate(small_image, large_image, method)

    mn, _, mnLoc, _ = cv2.minMaxLoc(result)
    print(cv2.minMaxLoc(result))

    MPx, MPy = mnLoc

    trows, tcols = small_image.shape[:2]

    cv2.rectangle(
        large_image,
        (MPx, MPy),
        (MPx+tcols, MPy+trows),
        (0, 255, 0),
        4
    )

    return large_image


def matching_object_scale(img_source, img_template):
    template = cv2.imread(img_template, 0)
    template = cv2.Canny(template, 50, 200)
    (tH, tW) = template.shape[:2]

    img_s = cv2.imread(img_source)
    gray = cv2.cvtColor(img_s, cv2.COLOR_BGR2GRAY)
    found = None

    for scale in np.linspace(0.2, 1.0, 30)[::-1]:
        resized = imutils.resize(gray, width=int(gray.shape[1] * scale))
        ratio = gray.shape[1] / float(resized.shape[1])

        # print(resized.shape, ratio)
        if resized.shape[0] < tH or resized.shape[1] < tW:
            break

        edge = cv2.Canny(resized, 50, 200)
        result = cv2.matchTemplate(edge, template, cv2.TM_CCOEFF)
        (_, max_val, _, max_loc) = cv2.minMaxLoc(result)

        if found is None or max_val > found[0]:
            found = (max_val, max_loc, ratio)

    (_, max_loc, ratio) = found
    (start_x, start_y) = (int(max_loc[0] * ratio), int(max_loc[1] * ratio))
    (end_x, end_y) = (
        int((max_loc[0] + tW) * ratio),
        int((max_loc[1] + tH) * ratio)
    )

    cv2.rectangle(
        img_s,
        (start_x, start_y),
        (end_x, end_y),
        (0, 0, 255),
        2
    )

    return img_s


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', required=True, help='Image source')
    parser.add_argument('-t', '--template', required=True,
                        help='Image template')
    args = parser.parse_args()

    source_path = args.source
    template_path = args.template

    # result = matching_object(source_path, template_path)
    result = matching_object_scale(source_path, template_path)

    show_window('Output', result)


if __name__ == "__main__":
    sys.exit(main())
