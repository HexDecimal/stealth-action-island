
import time

import tcod

import gameobj

#FONT = 'data/terminal8x8_gs_ro.png'
FONT = 'data/terminal8x12_gs_ro.png'

console = None

class Positional(object):
    def __init__(self, x, y, **kargs):
        super().__init__(**kargs)
        self.x = x
        self.y = y

class SimpleGraphic(object):
    def __init__(self, ch, fg, **kargs):
        super().__init__(**kargs)
        self.ch = ch
        self.fg = fg

class Player(Positional, SimpleGraphic):
    def __init__(self, **kargs):
        super().__init__(ch=ord('@'), fg=(255, 255, 255), **kargs)

DIR_KEYS = {
    tcod.KEY_UP: (0, -1),
    tcod.KEY_DOWN: (0, 1),
    tcod.KEY_LEFT: (-1, 0),
    tcod.KEY_RIGHT: (1, 0),

    tcod.KEY_KP1: (-1, 1),
    tcod.KEY_KP2: (0, 1),
    tcod.KEY_KP3: (1, 1),
    tcod.KEY_KP4: (-1, 0),
    tcod.KEY_KP6: (1, 0),
    tcod.KEY_KP7: (-1, -1),
    tcod.KEY_KP8: (0, -1),
    tcod.KEY_KP9: (1, -1),
    }

def draw():
    cam_x, cam_y = world.camera
    cam_width, cam_height = console.width, console.height
    cam_x -= cam_width // 2
    cam_y -= cam_height // 2
    console.ch[:], console.fg[:], console.bg[:] = \
        world.terrain.get_graphic(cam_x, cam_y, cam_width, cam_height)

    for obj in world.objects.area(cam_x, cam_y, cam_width, cam_height):
        if gameobj.Graphic not in obj:
            continue
        x, y = obj[gameobj.Location].xy
        x -= cam_x
        y -= cam_y
        console.ch[y, x] = obj[gameobj.Graphic].ch
        console.fg[y, x] = obj[gameobj.Graphic].fg
    tcod.console_flush()

def main():
    global console, world
    tcod.console_set_custom_font(
        FONT,
        tcod.FONT_LAYOUT_ASCII_INROW | tcod.FONT_TYPE_GREYSCALE,
        16, 16
        )
    console = tcod.console_init_root(60, 40, 'Test', False)

    world = gameobj.World()
    player = gameobj.GameObj(world)
    player[gameobj.Location].move(0, 0)
    player[gameobj.Graphic].ch = ord('@')

    while not tcod.console_is_window_closed():
        draw()
        key = tcod.console_wait_for_keypress(False)
        def inverse_key_const(vk):
            for attr in dir(tcod):
                if attr.startswith('KEY_') and getattr(tcod, attr) == vk:
                    return attr
        print((inverse_key_const(key.vk), key.c, key.text))
        if key.vk in DIR_KEYS:
            player[gameobj.Location].move_by(*DIR_KEYS[key.vk])
            world.camera = player[gameobj.Location].xy
