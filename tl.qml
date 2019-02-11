import QtQuick 2.0

Rectangle {
    id: page
    width: 400; height: 500
    color: "gray"

    Text {
        id: tlText
        text: "Tower lamp status"
        y: 30
        anchors.horizontalCenter: page.horizontalCenter
        font.pointSize: 24; font.bold: true
        color: "white"

        MouseArea {
            id: mouseArea
            anchors.fill: parent
        }

        states: State {
            name: "down"
            when: mouseArea.pressed == true
            PropertyChanges {
                target: tlText
                y: 160
                rotation: 180
                color: "red"
            }
        }

        transitions: Transition {
            from: ""; to: "down"; reversible: true
            ParallelAnimation {
                NumberAnimation {
                    properties: "y,rotation"
                    duration: 500
                    easing.type: Easing.InOutQuad
                }

                ColorAnimation {
                    duration: 500
                }
            }
        }
        
    }

    Grid {
        id: tlColors
        x: 4
        anchors.horizontalCenter: page.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        anchors.bottomMargin: 3
        anchors.topMargin: 3
        rows: 3; columns: 1; spacing: 3

        Cell { cellColor: "red"; onClicked: tlText.color = cellColor}
        Cell { cellColor: "yellow"; onClicked: tlText.color = cellColor}
        Cell { cellColor: "green"; onClicked: tlText.color = cellColor}
    }
}