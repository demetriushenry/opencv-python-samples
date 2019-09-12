import sys

import cv2


def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    # zoom range values 100 ~ 500 percent
    cap.set(cv2.CAP_PROP_ZOOM, 100)

    while True:
        ret, frame = cap.read()

        if ret:
            print('ZOOM:', cap.get(cv2.CAP_PROP_ZOOM))
            cv2.namedWindow('Frame', cv2.WINDOW_KEEPRATIO)
            cv2.imshow('Frame', frame)
        else:
            break

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    sys.exit(main())
