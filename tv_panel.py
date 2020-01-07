import sys

import cv2
import numpy as np


def view_image(name, frame):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.imshow(name, frame)


def get_img_range_hsv(img_hsv_path):
    img_mask = cv2.imread(img_hsv_path)
    img_hsv = cv2.cvtColor(img_mask, cv2.COLOR_BGR2HSV)
    min = [
        int(img_hsv[..., 0].min()),
        int(img_hsv[..., 1].min()),
        int(img_hsv[..., 2].min())
    ]
    max = [
        int(img_hsv[..., 0].max()),
        int(img_hsv[..., 1].max()),
        int(img_hsv[..., 2].max())
    ]
    return (np.array(min), np.array(max))


def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs(np.dot(d1, d2) / np.sqrt(np.dot(d1, d1)*np.dot(d2, d2)))


def find_squares(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # get threshold
    blur = cv2.GaussianBlur(gray, (7, 7), 15)
    _, threshold = cv2.threshold(
        blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # find contours
    squares = []
    cnts, _ = cv2.findContours(
        threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in cnts:
        cnt_len = cv2.arcLength(cnt, True)
        cnt = cv2.approxPolyDP(cnt, 0.1 * cnt_len, True)
        if len(cnt) == 4 and cv2.contourArea(cnt) > 300000 \
                and cv2.isContourConvex(cnt):
            cnt = cnt.reshape(-1, 2)
            max_cos = np.max(
                [angle_cos(
                    cnt[i],
                    cnt[(i+1) % 4],
                    cnt[(i+2) % 4]
                ) for i in range(4)]
            )
            if max_cos < 1.0:
                squares.append(cnt)

    # draw contours
    # color = (255, 0, 255)
    # if (squares):
    #     cv2.drawContours(frame, [squares[0]], 0, color, -1)
    return squares


def find_hsv_mask(frame, lower, upper):
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(frame_hsv, lower, upper)

    ones = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, ones, iterations=5)
    mask = cv2.dilate(mask, ones, iterations=1)

    mask = cv2.bitwise_not(mask)

    result = cv2.bitwise_and(frame, frame, mask=mask)
    result[mask == 0] = ([255, 255, 255])

    return mask


def main():
    video_path = 'videos/clean-panel-1.mp4'
    cap = cv2.VideoCapture(video_path)

    (lower, upper) = get_img_range_hsv('images/rolo-rosa.jpg')

    color = (255, 0, 255)
    square = None

    while True:
        ret, frame = cap.read()

        if ret:
            hsv_mask = find_hsv_mask(frame.copy(), lower, upper)

            if square is None:
                square = find_squares(frame.copy())
            else:
                cv2.drawContours(frame, [square[0]], 0, color, 3)

            view_image('hsv mask', hsv_mask)
            view_image('frame', frame)
        else:
            break

        if cv2.waitKey(22) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    sys.exit(main())
