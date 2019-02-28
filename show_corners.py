import subprocess
import sys

import cv2


def get_screen_resolution():
    output = subprocess.Popen(
        'xrandr | grep "\*" | cut -d" " -f4',
        shell=True,
        stdout=subprocess.PIPE
    ).communicate()[0]

    resolution = output.split()[0].split(b'x')

    return int(resolution[0]), int(resolution[1])


def show_corners(img_path):
    gray = cv2.imread(img_path, 0)
    gaussian = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gaussian, 35, 125)

    show_window('Gaussian', gaussian)
    show_window('Edges', edged)


def show_window(name_window, img_mat):
    res_w, res_h = get_screen_resolution()

    ratio = 3

    cv2.namedWindow(name_window, cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow(name_window, int(res_w // ratio), int(res_h // ratio))
    cv2.imshow(name_window, img_mat)


def main():
    img_path = '/home/demetrius/Comp/rois/roi_3.png'
    show_corners(img_path)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    sys.exit(main())
