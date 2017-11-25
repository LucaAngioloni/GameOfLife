from PyQt5.QtCore import QTimer


class GolLoop(QTimer):
    """
    Game of Life main loop class.

    Attributes:
        going   bool value representing the state of the game
        currentTimer    value of time between GoL steps in ms

    Fires timeout signal every currentTimer ms. Game of Life and View controllers are connected to this signal.
    """

    def __init__(self):
        super().__init__()

        self.going = False

        self.currentTimer = 100
        self.timeout.connect(self.loop)
        self.setSingleShot(True)  # so that the timer timeout fires only once when started

    def loop(self):
        """Main method: called at each timeout and if the game is playing restarts the timer with currentTimer value"""
        if self.going and self.isSingleShot() and self.currentTimer > 0:
            self.start(self.currentTimer)

    def set_speed(self, speed):
        """Setter for currentTimer(speed)"""
        self.currentTimer = speed

    def play_pause(self):
        """Toggle between play(going) and pause(!going) modes"""
        self.stop()
        self.going = not self.going
        if self.going is True:
            self.start(self.currentTimer)

    def is_going(self):
        """Getter for the state of the game"""
        return self.going
