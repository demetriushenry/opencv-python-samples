import sys
import cv2
import numpy as np


def method_1(frame):
    a = np.double(frame)
    b = a + 15
    img2 = np.uint8(b)
    return img2


def method_2(frame, gamma=1.0):
    invGamma = 1.0 / gamma
    table = np.array([
      ((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)])
    return cv2.LUT(frame.astype(np.uint8), table.astype(np.uint8))


def main():
    original = cv2.imread('/home/demetrius/Pictures/roi/modelo.jpg', 1)
    res_method_1 = method_1(original)
    res_method_2 = method_2(original, 0.5)

    cv2.namedWindow('Original', cv2.WINDOW_KEEPRATIO)
    # cv2.namedWindow('Result method 1', cv2.WINDOW_KEEPRATIO)
    cv2.namedWindow('Result method 2', cv2.WINDOW_KEEPRATIO)
    cv2.imshow('Original', original)
    # cv2.imshow('Result method 1', res_method_1)
    cv2.imshow('Result method 2', res_method_2)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    sys.exit(main())
