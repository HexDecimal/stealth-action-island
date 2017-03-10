
import time

import tcod

import state
import g
import gameobj
import world

#FONT = 'data/terminal8x8_gs_ro.png'
FONT = 'data/terminal8x12_gs_ro.png'
TITLE = 'title'

WIDTH = 1024 // 8
HEIGHT = 576 // 12

def main():
    g.world = world.World()
    g.player = gameobj.GameObj(g.world)
    g.player[gameobj.Location].move(0, 0)
    g.player[gameobj.Graphic].ch = ord('@')

    test = gameobj.GameObj(g.world)
    test[gameobj.Location].move(2, 0)
    test[gameobj.Graphic].ch = ord('U')

    tcod.console_set_custom_font(
        FONT,
        tcod.FONT_LAYOUT_ASCII_INROW | tcod.FONT_TYPE_GREYSCALE,
        16, 16
        )
    with tcod.console_init_root(WIDTH, HEIGHT, TITLE, False) as g.console:
        tcod.sys_set_fps(60)
        current_state = state.GameState()
        current_state.push()
