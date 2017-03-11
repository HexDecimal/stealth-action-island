
import time

import tcod

import state
import g
import obj
import world

#FONT = 'data/terminal8x8_gs_ro.png'
FONT = 'data/terminal8x12_gs_ro.png'
TITLE = 'title'

WIDTH = 1024 // 8
HEIGHT = 576 // 12

def main():
    g.world = world.World()
    g.player = obj.GameObj(g.world)
    g.player.location.move(0, 0)
    g.player.graphic.ch = ord('@')
    g.player.actor = obj.ActorPlayerControl(obj=g.player)

    test = obj.GameObj(g.world)
    test.location.move(2, 0)
    test.graphic.ch = ord('U')
    test.actor = obj.ActorTest(obj=test)

    tcod.console_set_custom_font(
        FONT,
        tcod.FONT_LAYOUT_ASCII_INROW | tcod.FONT_TYPE_GREYSCALE,
        16, 16
        )
    with tcod.console_init_root(WIDTH, HEIGHT, TITLE, False) as g.console:
        tcod.sys_set_fps(60)
        g.world.loop()
        current_state = state.GameState()
        current_state.push()
