##
## MIT License
## 
## Copyright (c) 2017 Luca Angioloni
## 
## Permission is hereby granted, free of charge, to any person obtaining a copy
## of this software and associated documentation files (the "Software"), to deal
## in the Software without restriction, including without limitation the rights
## to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
## copies of the Software, and to permit persons to whom the Software is
## furnished to do so, subject to the following conditions:
## 
## The above copyright notice and this permission notice shall be included in all
## copies or substantial portions of the Software.
## 
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
## OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
## SOFTWARE.
##

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
