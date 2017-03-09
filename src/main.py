
import time

import tcod

import state
import gameobj

#FONT = 'data/terminal8x8_gs_ro.png'
FONT = 'data/terminal8x12_gs_ro.png'

console = None
player = None

def main():
    global console, world, player
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

    test = gameobj.GameObj(world)
    test[gameobj.Location].move(2, 0)
    test[gameobj.Graphic].ch = ord('U')

    current_state = state.GameState()
    current_state.push()
