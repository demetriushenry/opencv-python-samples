import argparse
import math
import sys
import utils

import cv2


def decode(scores, geometry, score_thresh):
    detections = []
    confidences = []
    height, width = scores.shape[2], scores.shape[3]

    for y in range(0, height):
        scores_data = scores[0][0][y]
        x0_data = geometry[0][0][y]
        x1_data = geometry[0][1][y]
        x2_data = geometry[0][2][y]
        x3_data = geometry[0][3][y]
        angles = geometry[0][4][y]

        for x in range(0, width):
            score = scores_data[x]
            if score < score_thresh:
                continue

            offset_x = x * 4.0
            offset_y = y * 4.0
            angle = angles[x]
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)
            h = x0_data[x] + x2_data[x]
            w = x1_data[x] + x3_data[x]

            offset = (
                [
                    offset_x + cos_a * x1_data[x] + sin_a * x2_data[x],
                    offset_y + sin_a * x1_data[x] + cos_a * x2_data[x]
                ]
            )

            p1 = (-sin_a * h + offset[0], -cos_a * h + offset[1])
            p2 = (-cos_a * w + offset[0], -sin_a * w + offset[1])
            center = (0.5 * (p1[0] + p2[0]), 0.5 * (p1[1] + p2[1]))

            detections.append((center, (w, h), -1 * angle * 180 / math.pi))
            confidences.append(float(score))

    return (detections, confidences)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True)
    args = parser.parse_args()

    input_img = args.input
    img = cv2.imread(input_img)

    conf_thresh = 0.5
    nms_thresh = 0.4
    print((img.shape[0] / 1000) / 100)
    input_w = int(img.shape[1] * 0.02) * 32
    input_h = int(img.shape[0] * 0.02) * 32
    print(input_w, input_h)
    model = '/home/demetrius/Downloads/frozen_east_text_detection.pb'

    detection_net = cv2.dnn.readNet(model)
    detection_layers = [
        'feature_fusion/Conv_7/Sigmoid',
        'feature_fusion/concat_3'
    ]

    img_h, img_w = img.shape[:2]
    ratio_w = img_w / float(input_w)
    ratio_h = img_h / float(input_h)

    blob = cv2.dnn.blobFromImage(
        img,
        1.0,
        (input_w, input_h),
        (123.68, 116.78, 103.94),
        True,
        False
    )

    detection_net.setInput(blob)
    detections = detection_net.forward(detection_layers)

    scores, geometry = detections[0], detections[1]
    rects, confidences = decode(scores, geometry, conf_thresh)

    indices = cv2.dnn.NMSBoxesRotated(
        rects, confidences, conf_thresh, nms_thresh)

    for i in indices:
        vertices = cv2.boxPoints(rects[i[0]])
        for j in range(4):
            vertices[j][0] *= ratio_w
            vertices[j][1] *= ratio_h
        for j in range(4):
            p1 = (vertices[j][0], vertices[j][1])
            p2 = (vertices[(j + 1) % 4][0], vertices[(j + 1) % 4][1])
            cv2.line(img, p1, p2, (0, 255, 0), 2, cv2.LINE_AA)

    res_w, res_h = utils.get_screen_resolution()
    cv2.namedWindow('Words', cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow('Words', int(res_w // 1.2), int(res_h // 1.2))
    cv2.imshow('Words', img)
    cv2.waitKey(0)


if __name__ == "__main__":
    sys.exit(main())