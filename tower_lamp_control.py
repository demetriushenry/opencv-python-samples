"""Control tower lamp module."""
import subprocess
import sys

from PySide2.QtWidgets import (QApplication, QDesktopWidget, QDialog,
                               QPushButton, QVBoxLayout)

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
        self.off_all = QPushButton('Turn off all')
        self.infinity_relay = QPushButton('Toogle relay infinity')

        layout = QVBoxLayout()
        layout.addWidget(self.red_lamp)
        layout.addWidget(self.yellow_lamp)
        layout.addWidget(self.green_lamp)
        layout.addWidget(self.buzzer)
        layout.addWidget(self.off_all)
        layout.addWidget(self.infinity_relay)

        self.setLayout(layout)

        self.red_lamp.clicked.connect(self.toggle_red_light)
        self.yellow_lamp.clicked.connect(self.toggle_yellow_light)
        self.green_lamp.clicked.connect(self.toggle_green_light)
        self.buzzer.clicked.connect(self.toggle_buzzer)
        self.off_all.clicked.connect(self.turn_off_all)
        self.infinity_relay.clicked.connect(self.toogle_relay_infinity)

        w, h = get_screen_resolution()
        self.setGeometry(0, 0, w // 6, h // 6)

        self._move_to_center()

        self.init_tower_lamp()

    def init_tower_lamp(self):
        """Start serial communication."""
        self.tl = TowerLamp('/dev/ttyUSB0')
        self.pulse = False

    def toggle_red_light(self):
        """Toggle red light."""
        self.tl.toggle_relay(
            TowerLamp.RELAY_1, not self.tl.is_relay_1_on, pulse=self.pulse)

    def toggle_yellow_light(self):
        """Toggle yellow light."""
        self.tl.toggle_relay(
            TowerLamp.RELAY_2, not self.tl.is_relay_2_on, pulse=self.pulse)

    def toggle_green_light(self):
        """Toggle green light."""
        self.tl.toggle_relay(
            TowerLamp.RELAY_3, not self.tl.is_relay_3_on, pulse=self.pulse)

    def toggle_buzzer(self):
        """Toggle buzzer."""
        self.tl.toggle_relay(
            TowerLamp.RELAY_4, not self.tl.is_relay_4_on, pulse=self.pulse)

    def turn_off_all(self):
        self.tl.turn_off_all_relay()

    def toogle_relay_infinity(self):
        self.tl.toogle_relay_infinity(not self.tl.is_relay_4_on)

    def _move_to_center(self):
        rect = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        rect.moveCenter(center)
        self.move(rect.topLeft())


def get_screen_resolution():
    output = subprocess.Popen(
        'xrandr | grep "*" | cut -d" " -f4',
        shell=True,
        stdout=subprocess.PIPE
    ).communicate()[0]

    resolution = output.split()[0].split(b'x')

    return int(resolution[0]), int(resolution[1])


def main():
    """Call main function."""
    app = QApplication(sys.argv)

    form = ControlApp()
    form.show()

    res = app.exec_()

    del form
    sys.exit(res)


if __name__ == "__main__":
    sys.exit(main())
