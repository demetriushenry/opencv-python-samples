import sys

import cv2
import numpy as np


def reorder(points):
    new_points = np.zeros_like(points)
    points = points.reshape((4, 2))
    add_point = points.sum(1)
    new_points[0] = points[np.argmin(add_point)]
    new_points[3] = points[np.argmax(add_point)]
    diff = np.diff(points, axis=1)
    new_points[1] = points[np.argmin(diff)]
    new_points[2] = points[np.argmax(diff)]
    return new_points


def warp_img(img, points, w, h, pad=20):
    points = reorder(points)
    pts1 = np.float32(points)
    pts2 = np.float32([0, 0], [w, 0], [0, h], [w, h])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    img_warp = cv2.warpPerspective(img, matrix, (w, h))
    img_warp = img_warp[
        pad:img_warp.shape[0] - pad,
        pad:img_warp.shape[1] - pad
    ]
    return img_warp


def find_distance(pts1, pts2):
    # using Pythagorean theorem
    return ((pts2[0] - pts1[0]) ** 2 + (pts2[1] - pts1[1]) ** 2) ** 0.5


def get_contours(img, thr1=100, thr2=100, show_cany=False, min_area=1000, filter=0, show_cnts=False):
    kernel = (5, 5)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, kernel, 1)
    canny = cv2.Canny(blur, thr1, thr2)
    kernel = np.ones((5, 5))
    dilate = cv2.dilate(canny, kernel, iterations=3)
    erode = cv2.erode(dilate, kernel, iterations=2)

    if show_cany:
        cv2.imshow('Canny Image', erode)

    cnts, _ = cv2.findContours(erode, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    final_cnts = []

    for i in cnts:
        area = cv2.contourArea(i)

        if area > min_area:
            perimeter = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * perimeter, True)
            bbox = cv2.boundingRect(approx)

            cnt = [len(approx), area, approx, bbox, i]
            if filter > 0:
                if len(approx) == filter:
                    final_cnts.append(cnt)
            else:
                final_cnts.append(cnt)

    final_cnts = sorted(final_cnts, key=lambda x: x[1], reverse=True)

    if show_cnts:
        for cnt in final_cnts:
            color = (0, 0, 255)
            cv2.drawContours(img, cnt[4], -1, color, 3)

    return img, final_cnts


def main():
    scale = 3
    A4_w = 210 * scale  # mm
    A4_h = 297 * scale  # mm
    path = 'images/A4-paper.jpeg'
    img = cv2.imread(path)

    img_cnts, cnts = get_contours(img, min_area=50000, filter=4)

    if len(cnts) != 0:
        print('entrou')
        biggest = cnts[0][2]
        img_warp = warp_img(img, biggest, A4_w, A4_h)
        img_cnts2, cnts2 = get_contours(
            img_warp,
            min_area=2000,
            filter=4,
            thr1=50,
            thr2=50,
            show_cnts=False
        )

        if len(cnts) != 0:
            for obj in cnts2:
                cv2.polylines(img_cnts2, [obj[2]], True, (0, 255, 0), 2)
                nPoints = reorder(obj[2])
                pts1 = nPoints[0][0] // scale
                pts2 = nPoints[1][0] // scale
                pts3 = nPoints[2][0] // scale
                nW = round((find_distance(pts1, pts2) / 10), 1)
                nH = round((find_distance(pts1, pts3) / 10), 1)
                cv2.arrowedLine(img_cnts2, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[1][0][0], nPoints[1][0][1]),
                                (255, 0, 255), 3, 8, 0, 0.05)
                cv2.arrowedLine(img_cnts2, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[2][0][0], nPoints[2][0][1]),
                                (255, 0, 255), 3, 8, 0, 0.05)
                x, y, w, h = obj[3]
                cv2.putText(img_cnts2, '{}cm'.format(nW), (x + 30, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                            (255, 0, 255), 2)
                cv2.putText(img_cnts2, '{}cm'.format(nH), (x - 70, y + h // 2), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                            (255, 0, 255), 2)

        cv2.imshow('A4', img_cnts2)

    img = cv2.resize(img, (0, 0), None, 0.5, 0.5)
    cv2.imshow('Original', img)
    cv2.waitKey(0)


if __name__ == "__main__":
    sys.exit(main())
