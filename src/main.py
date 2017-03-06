
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
    }

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
        console.clear()
        for obj in world.objects.area(0, 0, console.width, console.height):
            if gameobj.Graphic not in obj:
                continue
            x, y = obj[gameobj.Location].xy
            console.ch[y, x] = player[gameobj.Graphic].ch
            console.fg[y, x] = player[gameobj.Graphic].fg
        tcod.console_flush()
        key = tcod.console_wait_for_keypress(False)
        print((key.vk, key.c, key.text))
        if key.vk in DIR_KEYS:
            obj[gameobj.Location].move_by(*DIR_KEYS[key.vk])
