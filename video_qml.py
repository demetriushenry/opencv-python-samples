"""original tutorial in C++
http://amin-ahmadi.com/2017/12/23/object-detection-using-qt-c-qml-opencv/
"""
import sys

import cv2
import numpy as np
from PySide2.QtCore import QCoreApplication, Qt, QUrl, Signal
from PySide2.QtGui import QGuiApplication, QImage
from PySide2.QtMultimedia import (QAbstractVideoBuffer, QAbstractVideoFilter,
                                  QVideoFilterRunnable, QVideoFrame)
from PySide2.QtQml import QQmlApplicationEngine, qmlRegisterType


class CvDetectFilter(QAbstractVideoFilter):
    objectDetected = Signal(float, float, float, float)

    def __init__(self, parent=None):
        QAbstractVideoFilter.__init__(self, parent)

    def create_filter_runnable(self):
        return CvDetectFilterRunnable(self)


class CvDetectFilterRunnable(QVideoFilterRunnable):

    def __init__(self, creator):
        self._filter = creator

    def run(self, input, surface_format, flags):
        input.map(QAbstractVideoBuffer.ReadOnly)

        if surface_format.handleType() == QAbstractVideoBuffer.NoHandle:
            image = QImage(
                input.bits(),
                input.width(),
                input.height(),
                QVideoFrame.imageFormatFromPixelFormat(input.pixelFormat())
            )
            image = image.convertToFormat(QImage.Format_RGB888)

            ptr = image.bits()
            ptr.setsize(image.count())

            matrix = np.array(ptr).reshape(
                image.height(),
                image.width(),
                QImage.Format_RGB888
            )

            matrix = cv2.flip(matrix, 0)

            classifier = cv2.CascadeClassifier(
                'data/haarcascade_frontalface_default.xml'
            )

            resized = image.size().scaled(320, 240, Qt.KeepAspectRatio)
            matrix = cv2.resize(matrix, (resized.width(), resized.height()))

            objs = classifier.detectMultiScale(matrix, 1.1)

            if len(objs) > 0:
                self._filter.objectDetected.emit(
                    float(objs[0].x) / float(matrix.cols),
                    float(objs[0].y) / float(matrix.rows),
                    float(objs[0].width) / float(matrix.cols),
                    float(objs[0].height) / float(matrix.rows)
                )
            else:
                self._filter.objectDetected.emit(0.0, 0.0, 0.0, 0.0)

        input.unmap()
        return input


def main():
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QGuiApplication(sys.argv)

    qmlRegisterType(CvDetectFilter, 'cvdetectfilter', 1, 0, 'CvDetectFilter')

    engine = QQmlApplicationEngine()
    engine.load(QUrl.fromLocalFile('video_qml.qml'))
    if not engine.rootObjects:
        sys.exit(-1)
    sys.exit(app.exec_())


if __name__ == "__main__":
    sys.exit(main())
