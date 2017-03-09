
import numpy as np
import tcod

import darray

TILES = np.zeros(
    256,
    dtype=[('ch', np.intc), ('fg', '(3,)u1'), ('bg', '(3,)u1')],
    )
TILES[0] = (0xf7, (0xff, 0xff, 0xff), (0x0, 0x0, 0xff))
TILES[1] = (ord('.'), (0xff, 0xff, 0xff), (0x0, 0x0, 0x0))
TILES[2] = (ord('^'), (0xff, 0xff, 0xff), (0x0, 0x0, 0x0))

class Terrain(object):
    def __init__(self):
        self.chunk_shape = (64, 64)
        self.tiles = darray.DynamicArray(self.chunk_shape, np.uint8,
                                         self.default_terrain)
        self.height_noise = tcod.noise.Noise(2)
        self.height_frequency = 16

    def default_terrain(self, mgrid):
        mgrid += 0xffff
        altitude = self.height_noise.sample_mgrid(mgrid / self.height_frequency)
        tiles = np.zeros(self.chunk_shape, np.uint8)
        tiles[altitude > -0.5] = 1
        tiles[altitude > 0.5] = 2
        return tiles

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
        tiles = self.tiles[y:y+height,x:x+width]
        tiles = TILES[tiles]
        return tiles['ch'], tiles['fg'], tiles['bg']
