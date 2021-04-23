import sys

import cv2


def view_image(name, img):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.imshow(name, img)


def main():
    img = cv2.imread('images/PanelInspection.png')

    # convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 5)

    # get adaptive threshhold
    # thresh = cv2.adaptiveThreshold(
    #     blur, 255,
    #     cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    #     cv2.THRESH_BINARY,
    #     141, 3
    # )
    thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1]

    # # apply morphologies
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    blob = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    blob = cv2.morphologyEx(blob, cv2.MORPH_CLOSE, kernel)

    # # invert blob
    blob = (255 - blob)

    # get contours
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    # big_contour = max(cnts, key=cv2.contourArea)

    # draw contours
    result = img.copy()
    # cv2.drawContours(result, [big_contour], 0, (0, 0, 255), -1)
    min_area = 50
    color = (0, 255, 0)
    for cnt in cnts:
        area = cv2.contourArea(cnt)
        if area > min_area:
            cv2.drawContours(result, [cnt], 0, color, 3)

    # show results
    view_image('Original', img)
    view_image('Threshold', thresh)
    view_image('Blob', blob)
    view_image('Result', result)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    sys.exit(main())
