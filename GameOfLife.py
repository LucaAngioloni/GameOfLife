import numpy as np
from scipy import ndimage
from PIL import Image
import os

PIXEL_MAX = 255

class GameOfLife:
    def __init__(self, x, y, mode='empty'):
        self.mode = mode
        self.x = x
        self.y = y
        self.mat = np.zeros((self.x, self.y), dtype=np.uint8)
        if self.mode == "random":
            rand_m = np.random.randn(self.x, self.y) - 0.5  # less white cells than black voids
            indexes_p = rand_m > 0
            self.mat[indexes_p] = PIXEL_MAX
        self.initial_state = np.copy(self.mat)

    def reset(self):
        self.mat = np.copy(self.initial_state)

    def reinitialize(self, x, y, state='empty'):
        self.mode = state
        self.x = x
        self.y = y
        self.reset()

    def load(self, fileName):
        # check if txt or png and proceed accordingly
        extension = os.path.splitext(fileName)[1][1:]
        if extension == "png":
            im_frame = Image.open(fileName).convert('L')
            width, height = im_frame.size
            self.x = height
            self.y = width
            np_frame = np.array(im_frame.getdata())
            np_frame = np.reshape(np_frame, (-1, width))
            self.mat = np.zeros(np_frame.shape, dtype=np.uint8)
            self.mat[np_frame > 128] = PIXEL_MAX
            self.initial_state = np.copy(self.mat)
            return True
        elif extension == "txt":
            print('txt')
            with open(fileName) as f:
                for i, l in enumerate(f):
                    pass
            rows = i + 1
            cols = len(l)

            self.mat = np.zeros((rows, cols), dtype=np.uint8)

            with open(fileName) as f:
                for j, line in enumerate(f):
                    for k, c in enumerate(line):
                        if c == "X":
                            self.mat[j, k] = PIXEL_MAX

            self.x = rows
            self.y = cols

            self.initial_state = np.copy(self.mat)
            return True
        else:
            print('Wrong file type')
            return False

    def save(self, fileName):
        # save as png
        extension = os.path.splitext(fileName)[1][1:]
        if extension == "png":
            path = fileName
        else:
            path = fileName + ".png"

        im = Image.fromarray(self.mat)
        im.save(path)

    def set_model(self, new_mat):
        self.mat = new_mat
        self.initial_state = np.copy(self.mat)

    def next(self):
        res = ndimage.uniform_filter(self.mat, size=3)
        res[self.mat > 128] = res[self.mat > 128] - int((1/9)*PIXEL_MAX)
        self.mat[res <= int((1/9)*PIXEL_MAX)] = 0
        self.mat[res >= int((4/9)*PIXEL_MAX)] = 0
        self.mat[res == int((3/9)*PIXEL_MAX)] = PIXEL_MAX

    def get_state(self):
        return self.mat



