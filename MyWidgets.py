import os
import sys

from PyQt5.QtWidgets import QComboBox, QPushButton

class PatternMenu(QComboBox):
    """
    Custom combo box widget that auto populates its items with patterns found in the default directory

    Attributes:
        path_to_patterns    default directory for patterns
        files               string list of the file names of the files in path_to_patterns
    """

    def __init__(self):
        super().__init__()
        self.path_to_patterns = os.path.abspath(os.path.dirname(sys.argv[0])) + "/patterns/"
        self.files = sorted([f for f in os.listdir(self.path_to_patterns) if not f.startswith('.')],
                            key=lambda f: f.lower())
        self.addItem("Empty")
        self.addItem("Random")
        self.addItems(self.files)


class PlayPauseButton(QPushButton):
    """
        Custom push button that toggles automatically Play and Pause texts

        Attributes:
            btn_text    list of the 2 strings ["Play", "Pause"]
        """
    def __init__(self):
        super().__init__()

        self.setFixedWidth(100)
        self.btn_text = ["Play", "Pause"]
        self.i = 0

        self.setText(self.btn_text[self.i])

        self.clicked.connect(self.changeText)

    def changeText(self):
        """Slot for the clicked event; automatically changes the button text"""
        self.i += 1
        self.setText(self.btn_text[self.i % 2])