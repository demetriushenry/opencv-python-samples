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


def find_squares(frame, size_area=300000):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # get threshold
    blur = cv2.GaussianBlur(gray, (7, 7), 15)
    _, threshold = cv2.threshold(
        blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # find contours
    squares = []
    cnts, _ = cv2.findContours(
        threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in cnts:
        cnt_len = cv2.arcLength(cnt, True)
        cnt = cv2.approxPolyDP(cnt, 0.1 * cnt_len, True)
        if len(cnt) == 4 and cv2.contourArea(cnt) > size_area \
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

    return squares, threshold


def find_hsv_mask(frame, lower, upper):
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(frame_hsv, lower, upper)

    ones = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, ones, iterations=5)
    mask = cv2.dilate(mask, ones, iterations=1)

    # mask = cv2.bitwise_not(mask)

    result = cv2.bitwise_and(frame, frame, mask=mask)
    result[mask == 0] = ([255, 255, 255])

    return mask, result


def find_hsv_squares(mask, size_area=10000):
    squares = []
    cnts, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in cnts:
        if cv2.contourArea(cnt) > size_area:
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            squares.append(box)

    return squares


def main():
    video_path = 'videos/clean-panel-2.mp4'
    cap = cv2.VideoCapture(video_path)

    (lower, upper) = get_img_range_hsv('images/rolo-rosa.jpg')

    tv_border_color = (255, 0, 255)
    obj_border_color = (0, 255, 0)
    tv_rect = None
    tv_thresh = None
    mask_tv = None
    mask_obj = None
    h = None
    w = None

    while True:
        ret, frame = cap.read()

        if ret:
            if not h and not w:
                h, w = frame.shape[:2]
            if mask_tv is None:
                mask_tv = np.zeros((h, w), np.uint8)
            if mask_obj is None:
                mask_obj = np.zeros((h, w), np.uint8)

            hsv_mask, result = find_hsv_mask(frame.copy(), lower, upper)

            # get and draw tv rectangle
            if tv_rect is None:
                tv_rect, tv_thresh = find_squares(frame.copy())
            else:
                cnt = [tv_rect[0]]
                # cv2.drawContours(frame, cnt, 0, tv_border_color, 3)
                cv2.drawContours(mask_tv, cnt, 0, (255, 255, 255), -1)

            # get and draw obj rectangle
            obj_rect = find_hsv_squares(hsv_mask)
            if obj_rect:
                cnt = [obj_rect[0]]
                # cv2.drawContours(frame, cnt, 0, obj_border_color, -1)
                cv2.drawContours(mask_obj, cnt, 0, (255, 255, 255), -1)

            # final mask
            # final_mask_1 = mask_tv - mask_obj
            final_mask = cv2.bitwise_and(mask_tv, mask_obj)
            final_mask = final_mask - mask_tv
            cnts, _ = cv2.findContours(
                final_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(frame, cnts, -1, tv_border_color, -1)

            # view_image('hsv mask', hsv_mask)
            # view_image('result', result)
            # view_image('thresh', tv_thresh)
            view_image('mask-tv', mask_tv)
            view_image('mask-obj', mask_obj)
            view_image('Final-mask', final_mask)
            view_image('frame', frame)
        else:
            break

        if cv2.waitKey(22) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    sys.exit(main())
