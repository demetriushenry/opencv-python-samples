import QtQuick 2.12

Rectangle {
    id: page
    width: 350; height: 450
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
        y: 110
        anchors.horizontalCenter: page.horizontalCenter
        rows: 3; columns: 1; spacing: 3

        Cell { cellColor: "red"}
        Cell { cellColor: "yellow"}
        Cell { cellColor: "green"}
    }
}