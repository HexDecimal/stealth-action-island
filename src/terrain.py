
import numpy as np
import tcod

class Terrain(object):
    def __init__(self):
        self.height_noise = tcod.noise.Noise(2)
        self.height_frequency = 16

    def get_ogrid(self, x, y, width, height):
        left = x / self.height_frequency
        right = left + width / self.height_frequency
        top = y / self.height_frequency
        bottom = top + height / self.height_frequency
        return (np.linspace(top, bottom, height, False),
                np.linspace(left, right, width, False),)

    def get_mgrid(self, x, y, width, height):
        x += 0xffff
        y += 0xffff
        return (np.mgrid[y:y+height,x:x+width].astype(np.float) /
                self.height_frequency)

    def get_graphic(self, x, y, width, height):
        ch = np.ndarray((height, width), np.intc)
        fg = np.ndarray((height, width, 3), np.uint8)
        bg = np.ndarray((height, width, 3), np.uint8)
        ch[:] = ord(' ')
        fg[:] = 255
        altitude = self.height_noise.sample_mgrid(self.get_mgrid(x, y, width, height))
        bg[:,:,0] = altitude * 120 + 127
        bg[:,:,2] = bg[:,:,1] = bg[:,:,0]
        return ch, fg, bg