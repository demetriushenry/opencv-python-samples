"""ex. python ocr_text_channels.py -i /home/demetrius/Pictures/procel_tag.jpg"""
import argparse
import sys
import time

import cv2
import numpy as np
import pytesseract as ocr
from PIL import Image


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True)
    args = parser.parse_args()

    input_img = args.input
    img = cv2.imread(input_img)

    # h, w = img.shape[:2]
    # img = cv2.resize(img, (w // 2, h // 2))

    # diminuição dos ruidos antes da binarização
    img[:, :, 0] = 0
    img[:, :, 2] = 0

    # escala de cinzas
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # binarizacao
    ret, thresh = cv2.threshold(
        img, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    cv2.namedWindow('Original', cv2.WINDOW_KEEPRATIO)
    cv2.imshow('Original', img)

    cv2.namedWindow('Thresh', cv2.WINDOW_KEEPRATIO)
    cv2.imshow('Thresh', thresh)

    # thresh = Image.fromarray(thresh)

    # tesseract config
    config = ('-l eng --oem 1 --psm 3')

    start = time.time()
    ocr_text = ocr.image_to_string(thresh, config=config)
    end = time.time()
    elapsed_time = end - start

    print(ocr_text)
    print('elapsed time:', elapsed_time)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    sys.exit(main())
