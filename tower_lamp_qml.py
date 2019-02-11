import sys

from PySide2.QtCore import QUrl
from PySide2.QtQuick import QQuickView
from PySide2.QtWidgets import QApplication

app = QApplication()
view = QQuickView()
url = QUrl("tl.qml")

view.setSource(url)
view.setTitle("Tower lamp status")
view.show()
res = app.exec_()

# ensure correct destruction for 
del view
sys.exit(res)
