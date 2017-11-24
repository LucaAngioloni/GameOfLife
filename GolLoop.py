from PyQt5.QtCore import QTimer


class GolLoop(QTimer):
    def __init__(self):
        super().__init__()

        self.going = False

        self.currentTimer = 100
        self.timeout.connect(self.loop)
        self.setSingleShot(True)

    def loop(self):
        if self.going and self.isSingleShot() and self.currentTimer > 0:
            self.setSingleShot(True)
            self.start(self.currentTimer)

    def set_speed(self, speed):
        self.currentTimer = speed

    def play_pause(self):
        self.stop()
        self.going = not self.going
        if self.going is True:
            self.setSingleShot(True)
            self.start(self.currentTimer)

    def is_going(self):
        return self.going