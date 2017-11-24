import numpy as np
from scipy import ndimage
from PIL import Image
import os


PIXEL_MAX = 255
DECAY = 0.9

class GameOfLife:
    def __init__(self, x=100, y=150, mode='empty'):
        self.reinitialize(mode, x, y)
        self.do_heatmap = False

    def set_do_heatmap(self, b):
        self.do_heatmap = b

    def reset(self):
        self.mat = np.copy(self.initial_state)
        self.heatmap = np.copy(self.mat)

    def reinitialize(self, mode='empty', x=100, y=150):
        self.mode = mode
        self.x = x
        self.y = y
        self.mat = np.zeros((self.x, self.y), dtype=np.uint8)
        if self.mode == 'random': # redo it better
            rand_m = np.random.randn(self.x, self.y) - 0.5  # less white cells than black voids
            indexes_p = rand_m > 0
            self.mat[indexes_p] = PIXEL_MAX
        self.initial_state = np.copy(self.mat)
        self.heatmap = np.copy(self.mat)

    def load(self, file_name):
        # check if txt or png and proceed accordingly
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
            with open(file_name) as f:
                for i, l in enumerate(f):
                    pass
            rows = i + 1
            cols = len(l)

            self.mat = np.zeros((rows, cols), dtype=np.uint8)

            with open(file_name) as f:
                for j, line in enumerate(f):
                    for k, c in enumerate(line):
                        if c == "X":
                            self.mat[j, k] = PIXEL_MAX

            self.x = rows
            self.y = cols

            self.initial_state = np.copy(self.mat)
            self.heatmap = np.copy(self.mat)
            return True
        else:
            print('Wrong file type')
            return False

    def save(self, file_name):
        # save as png
        extension = os.path.splitext(file_name)[1][1:]
        if extension == "png":
            path = file_name
        else:
            path = file_name + ".png"

        im = Image.fromarray(self.mat)
        im.save(path)

    def set_model(self, new_mat):
        self.mat = new_mat
        self.initial_state = np.copy(self.mat)
        self.heatmap = np.copy(self.mat)

    def next(self):
        res = ndimage.uniform_filter(self.mat, size=3, mode='constant', cval=0)
        res[self.mat > 128] = res[self.mat > 128] - int((1/9)*PIXEL_MAX)
        self.mat[res <= int((1/9)*PIXEL_MAX)] = 0
        self.mat[res >= int((4/9)*PIXEL_MAX)] = 0
        self.mat[res == int((3/9)*PIXEL_MAX)] = PIXEL_MAX
        self.heatmap = np.array(self.heatmap * DECAY, dtype=np.uint8)
        self.heatmap[self.mat > 128] = PIXEL_MAX

    def get_state(self):
        if self.do_heatmap:
            return self.heatmap
        else:
            return self.mat

    def set_active_cell(self, i, j):
        self.mat[i, j] = PIXEL_MAX
        self.heatmap[i, j] = PIXEL_MAX

    def set_inactive_cell(self, i, j):
        self.mat[i, j] = 0
        self.heatmap[i, j] = 0
