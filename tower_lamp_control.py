"""Control tower lamp module."""
import sys

from PySide2.QtWidgets import (QApplication, QDialog, QLineEdit, QPushButton,
                               QVBoxLayout)

from tower_lamp import TowerLamp


class ControlApp(QDialog):
    """Tower lamp control class.
    
    Arguments:
        QDialog {QDialog} -- parent class
    """

    def __init__(self, parent=None):
        """Control app constructor.
        
        Keyword Arguments:
            parent {QObject} -- parent QObject (default: {None})
        """
        super(ControlApp, self).__init__(parent)

        self.setWindowTitle('Control Tower lamp')

        self.red_lamp = QPushButton('Toggle red light')
        self.yellow_lamp = QPushButton('Toggle yellow light')
        self.green_lamp = QPushButton('Toggle green light')
        self.buzzer = QPushButton('Toggle buzzer')

        layout = QVBoxLayout()
        layout.addWidget(self.red_lamp)
        layout.addWidget(self.yellow_lamp)
        layout.addWidget(self.green_lamp)
        layout.addWidget(self.buzzer)

        self.setLayout(layout)

        self.red_lamp.clicked.connect(self.toggle_red_light)
        self.yellow_lamp.clicked.connect(self.toggle_yellow_light)
        self.green_lamp.clicked.connect(self.toggle_green_light)
        self.buzzer.clicked.connect(self.toggle_buzzer)

        self.init_tower_lamp()

    def init_tower_lamp(self):
        self.tl = TowerLamp('/dev/ttyUSB0')

    def toggle_red_light(self):
        self.tl.toggle_relay(TowerLamp.RELAY_1, not self.tl.is_relay_1_on)

    def toggle_yellow_light(self):
        self.tl.toggle_relay(TowerLamp.RELAY_2, not self.tl.is_relay_2_on)

    def toggle_green_light(self):
        self.tl.toggle_relay(TowerLamp.RELAY_3, not self.tl.is_relay_3_on)

    def toggle_buzzer(self):
        self.tl.toggle_relay(TowerLamp.RELAY_4, not self.tl.is_relay_4_on)


def main():
    """Call main function."""
    app = QApplication(sys.argv)
    
    form = ControlApp()
    form.show()

    app.exec_()


if __name__ == "__main__":
    sys.exit(main())
