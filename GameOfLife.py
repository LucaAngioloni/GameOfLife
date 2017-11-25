import os

import numpy as np
from PIL import Image
from scipy import ndimage

PIXEL_MAX = 255  # Constant representing the value of alive cells pixels (matrix elements)
DECAY = 0.9  # Constant representing the decay rate of past states when calculating the heat map


class GameOfLife:
    """
    This class contains the game state and the rules of the game. (The Model)

    It provides methods to get, set, modify and evolve the state following the rules.

    It also provides methods to load and save the state from and to file.

    Attributes:
        mat             current state of the game
        heatmap         weighted average of past states (history of past states)
        do_heatmap      boolean value defining what to return in get_state (the state or the heatmap)
        x, y            current board dimensions
        initial_state   backed up initial state that becomes the state when/if reset
    """

    def __init__(self, x=100, y=150, mode='empty'):
        """
        Init method.

        Args:
            x, y    default dimensions of the game board
            mode    default initial game mode: empty or random
        """
        self.reinitialize(mode, x, y)
        self.do_heatmap = False

    def set_do_heatmap(self, b):
        """Setter for the boolean attribute do_heatmap"""
        self.do_heatmap = b

    def reinitialize(self, mode='empty', x=100, y=150):
        """
        This method initializes the class attributes to the default values

        Args:
            x, y    default dimensions of the game board
            mode    default initial game mode: empty or random
        """
        self.mode = mode
        self.x = x
        self.y = y
        self.mat = np.zeros((self.x, self.y), dtype=np.uint8)
        if self.mode == 'random':  # redo it better
            rand_m = np.random.randn(self.x, self.y) - 0.5  # less white cells than black voids
            indexes_p = rand_m > 0
            self.mat[indexes_p] = PIXEL_MAX
        self.initial_state = np.copy(self.mat)
        self.heatmap = np.copy(self.mat)

    def reset(self):
        """Resets the state of the game to the backed up initial_state"""
        self.mat = np.copy(self.initial_state)
        self.heatmap = np.copy(self.mat)

    def next(self):
        """
        This method is the engine of the game. Calculates and updates the next state of the game following the rules.
        It also updates the heatmap state.
        """
        res = ndimage.uniform_filter(self.mat, size=3, mode='constant', cval=0)
        res[self.mat > 128] = res[self.mat > 128] - int((1 / 9) * PIXEL_MAX)
        self.mat[res <= int((1 / 9) * PIXEL_MAX)] = 0
        self.mat[res >= int((4 / 9) * PIXEL_MAX)] = 0
        self.mat[res == int((3 / 9) * PIXEL_MAX)] = PIXEL_MAX
        self.heatmap = np.array(self.heatmap * DECAY, dtype=np.uint8)
        self.heatmap[self.mat > 128] = PIXEL_MAX

    def get_state(self):
        """Getter for the current state which can be the state matrix ot the heatmap matrix depending on do_heatmap"""
        if self.do_heatmap:
            return self.heatmap
        else:
            return self.mat

    def set_active_cell(self, i, j):
        """Sets the cell at position (i, j) to be active(alive)"""
        self.mat[i, j] = PIXEL_MAX
        self.heatmap[i, j] = PIXEL_MAX

    def set_inactive_cell(self, i, j):
        """Sets the cell at position (i, j) to be inactive(dead)"""
        self.mat[i, j] = 0
        self.heatmap[i, j] = 0

    def load(self, file_name):
        """
        Loads the state from file.

        Args:
            file_name   name of the file. It can be a TXT (with known format) or PNG file

        Returns:
            bool        True for success (file existing and correct format), False otherwise.
        """
        extension = os.path.splitext(file_name)[1][1:]
        if extension == "png":
            im_frame = Image.open(file_name).convert('L')
            width, height = im_frame.size
            self.x = height
            self.y = width
            np_frame = np.array(im_frame.getdata())
            np_frame = np.reshape(np_frame, (-1, width))
            self.mat = np.zeros(np_frame.shape, dtype=np.uint8)
            self.mat[np_frame > 128] = PIXEL_MAX
            self.initial_state = np.copy(self.mat)
            self.heatmap = np.copy(self.mat)
            return True
        elif extension == "txt":
            rows = 0
            cols = 0
            with open(file_name) as f:
                for i, l in enumerate(f):
                    if l[0] != "#":
                        rows += 1
                        if len(l) > cols:
                            cols = len(l)

            self.mat = np.zeros((rows, cols), dtype=np.uint8)

            hash_rows = 0
            with open(file_name) as f:
                for j, line in enumerate(f):
                    for k, c in enumerate(line):
                        if c == "#" and k is 0:
                            hash_rows += 1
                            break
                        elif c != "." and c != "\n":
                            self.mat[j-hash_rows, k] = PIXEL_MAX

            self.x = rows
            self.y = cols

            self.initial_state = np.copy(self.mat)
            self.heatmap = np.copy(self.mat)
            return True
        else:
            print('Wrong file type')
            return False

    def save(self, file_name):
        """
        Saves the state to a PNG file.

        Args:
            file_name   name of the file to be saved as PNG (1 channel)
        """
        extension = os.path.splitext(file_name)[1][1:]
        if extension == "png":
            path = file_name
        else:
            path = file_name + ".png"

        im = Image.fromarray(self.mat)
        im.save(path)
