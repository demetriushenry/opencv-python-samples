import QtQuick 2.12

Item {
    id: container
    property alias cellColor: rectangle.color
    // signal clicked(color cellColor)

    width: 100; height: 100

    Rectangle {
        id: rectangle
        // border.color: "white"
        anchors.fill: parent

        MouseArea {
            id: rectangleArea
            anchors.fill: parent
            onClicked: {
                if (!cellAnim.running) {
                    cellAnim.start()
                } else {
                    cellAnim.complete()
                    cellAnim.stop()
                }
            }
        }        

        SequentialAnimation {
            id: cellAnim
            running: false
            loops: Animation.Infinite
            OpacityAnimator { target: rectangle; from: 1; to: 0; duration: 1000 }
            OpacityAnimator { target: rectangle; from: 0; to: 1; duration: 1000 }
        }
    }
}