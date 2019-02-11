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
        font.pointSize: 24; font.bold: false
        color: "white"
    }

    Grid {
        id: tlColors
        anchors.horizontalCenter: page.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        rows: 3; columns: 1; spacing: 3

        Cell { cellColor: "red"; onClicked: tlText.color = cellColor}
        Cell { cellColor: "yellow"; onClicked: tlText.color = cellColor}
        Cell { cellColor: "green"; onClicked: tlText.color = cellColor}
    }
}