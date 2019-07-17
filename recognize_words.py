"""ex. python recognize_words.py -i /home/demetrius/Pictures/procel_tag.jpg"""
import argparse
import sys

import cv2
import numpy as np
import pytesseract
from imutils.object_detection import non_max_suppression


def decode(scores, geometry, score_thresh):
    detections = []
    confidences = []
    height, width = scores.shape[2:4]

    for y in range(0, height):
        scores_data = scores[0, 0, y]
        x0_data = geometry[0, 0, y]
        x1_data = geometry[0, 1, y]
        x2_data = geometry[0, 2, y]
        x3_data = geometry[0, 3, y]
        angles = geometry[0, 4, y]

        for x in range(0, width):
            score = scores_data[x]
            if score < score_thresh:
                continue

            offset_x, offset_y = (x * 4.0, y * 4.0)

            angle = angles[x]
            cos = np.cos(angle)
            sin = np.sin(angle)

            h, w = ((x0_data[x] + x2_data[x]), (x1_data[x] + x3_data[x]))

            final_x = int(offset_x + (cos * x1_data[x]) + (sin * x2_data[x]))
            final_y = int(offset_y - (sin * x1_data[x]) + (cos * x2_data[x]))
            start_x = int(final_x - w)
            start_y = int(final_y - h)

            detections.append((start_x, start_y, final_x, final_y))
            confidences.append(score)

    return (detections, confidences)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=True)
    parser.add_argument('-p', '--padding', type=float, default=0.0)
    args = parser.parse_args()

    input_img = args.input
    input_padding = args.padding

    img = cv2.imread(input_img)
    orig = img.copy()
    orig_h, orig_w = img.shape[:2]

    input_w = int(img.shape[1] * 0.02) * 32
    input_h = int(img.shape[0] * 0.02) * 32
    ratio_w = orig_w / float(input_w)
    ratio_h = orig_h / float(input_h)

    img = cv2.resize(img, (input_w, input_h))
    img_h, img_w = img.shape[:2]

    conf_thresh = 0.5
    model = 'data/frozen_east_text_detection.pb'

    detection_net = cv2.dnn.readNet(model)
    detection_layers = [
        'feature_fusion/Conv_7/Sigmoid',
        'feature_fusion/concat_3'
    ]

    blob = cv2.dnn.blobFromImage(
        img,
        1.0,
        (img_w, img_h),
        (123.68, 116.78, 103.94),
        True,
        False
    )

    detection_net.setInput(blob)
    (scores, geometry) = detection_net.forward(detection_layers)
    (rects, confidences) = decode(scores, geometry, conf_thresh)
    boxes = non_max_suppression(np.array(rects), probs=confidences)

    results = []
    for (x1, y1, x2, y2) in boxes:
        x1 = int(x1 * ratio_w)
        y1 = int(y1 * ratio_h)
        x2 = int(x2 * ratio_w)
        y2 = int(y2 * ratio_h)

        dx = int((x2 - x1) * input_padding)
        dy = int((y2 - y1) * input_padding)

        x1 = max(0, x1 - dx)
        y1 = max(0, y1 - dy)
        x2 = min(orig_w, x2 + (dx * 2))
        y2 = min(orig_h, y2 + (dy * 2))

        roi = orig[y1:y2, x1:x2]

        tess_config = ("-l eng --oem 1 --psm 7")
        text = pytesseract.image_to_string(roi, config=tess_config)
        results.append(((x1, x1, x2, y2), text))

    # results = sorted(results, key=lambda r: r[0][1])
    out = orig.copy()
    for ((x1, y1, x2, y2), text) in results:
        print(text)
        cv2.rectangle(
            out,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2,
            cv2.LINE_AA
        )

    cv2.namedWindow('Words', cv2.WINDOW_KEEPRATIO)
    cv2.imshow('Words', out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    sys.exit(main())
