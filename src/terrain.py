
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

class HeightMap(object):
    def __init__(self, terrain):
        self.terrain = terrain
        self.height_noise = tcod.noise.Noise(2)
        self.height_frequency = terrain.radius / 3

    def __getitem__(self, mgrid):
        mgrid = mgrid.astype(np.float32)
        distance = np.hypot(*mgrid)
        altitude = -distance / self.terrain.radius * 2.5 + 1
        mgrid += 0xffff

        altitude += self.height_noise.sample_mgrid(mgrid /
                                                   self.height_frequency)
        return altitude

class Terrain(object):
    def __init__(self):
        self.radius = 1000
        self.chunk_shape = (256, 256)
        self.tiles = darray.DynamicArray(self.chunk_shape, np.uint8,
                                         self.default_terrain)
        self.altitude = HeightMap(self)

    def default_terrain(self, mgrid):
        altitude = self.altitude[mgrid]
        tiles = np.zeros(altitude.shape, np.uint8)
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
        return (np.mgrid[y:y+height,x:x+width])

    def get_map_graphic(self, width, height):
        ratio_width = max(1, width / height)
        ratio_height = max(1, height / width)
        mgrid = np.asarray(
            np.meshgrid(
                np.linspace(-self.radius * ratio_width,
                            self.radius * ratio_width, width, False),
                np.linspace(-self.radius * ratio_height,
                            self.radius * ratio_height, height, False),
                )
            )
        altitude = self.altitude[mgrid]
        altitude_color = (altitude + 1) * 127
        #ch = np.empty((height, width), np.intc)
        #ch = ord(' ')
        #fg = np.empty((height, width, 3), np.uint8)
        #fg[:] = (255, 255, 255)
        bg = np.empty((height, width, 3), np.uint8)
        bg[:,:,0] = altitude_color.clip(0, 255)
        bg[:,:,2] = bg[:,:,1] = bg[:,:,0]
        bg[altitude < -0.5] = (0, 0, 255)
        return ord(' '), (255, 255, 255), bg

    def get_graphic(self, x, y, width, height):
        tiles = self.tiles[y:y+height,x:x+width]
        tiles = TILES[tiles]
        return tiles['ch'], tiles['fg'], tiles['bg']
