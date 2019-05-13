import QtQuick 2.10
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.3
import QtMultimedia 5.8
import cvdetectfilter 1.0

ApplicationWindow {
    visible: true
    width: 800
    height: 600
    title: qsTr("Cv Detector")

    CvDetectFilter {
        id: testFilter

        // onObjectDetected: {
        //     if((w == 0) || (h == 0)) {
        //         smile.visible = false;
        //     } else {
        //         var r = video.mapNormalizeRectToItem(Qt.rect(x, y, w, h));
        //         smile.x = r.x;
        //         smile.y = r.y;
        //         smile.width = r.width;
        //         smile.height = r.height;
        //         smile.visible = true;
        //     }
        // }
    }

    Camera {
        id: camera
    }

    ShaderEffect {
        id: videoShader
        property variant src: video
        property variant source: video
    }

    ColumnLayout {
        
        anchors.fill: parent

        VideoOutput {
            id: video
            Layout.fillHeight: true
            Layout.fillWidth: true
            source: camera
            autoOrientation: false

            filters: [testFilter]

            Image {
                id: smile
                source: "images/smile.png"
                visible: false
            }
        }

        RowLayout {
            Layout.alignment: Qt.AlignHCenter
            Layout.fillWidth: true

            Label {
                text: "Camera"
            }

            ComboBox {
                Layout.fillWidth: true
                model: QtMultimedia.availableCameras
                textRole: "displayName"

                onActivated: {
                    camera.stop()
                    camera.deviceId = model[currentIndex].deviceId
                    cameraStartTimer.start()
                }

                Timer {
                    id: cameraStartTimer
                    interval: 500
                    running: false
                    repeat: false
                    onTriggered: camera.start()
                }

                onAccepted: {
                    console.log("selected")
                }
            }
        }
    }
}
