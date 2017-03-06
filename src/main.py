
import time

import tcod

import ecs

#FONT = 'data/terminal8x8_gs_ro.png'
FONT = 'data/terminal8x12_gs_ro.png'

console = None

class Position(ecs.Component):
    def __init__(self, entity, x, y):
        super().__init__(entity)
        self.x = x
        self.y = y

class OldGraphicPosition(Position):
    pass

class Graphic(ecs.Component):
    def __init__(self, entity, ch, fg):
        self.ch = ch
        self.fg = fg
        super().__init__(entity)

class RendererSystem(ecs.System):
    def ev_added(self, component):
        if isinstance(component, Graphic):
            pos, = component.entity[Position]
            console.ch[pos.y, pos.x] = component.ch
            console.fg[pos.y, pos.x] = component.fg

def main():
    global console
    tcod.console_set_custom_font(
        FONT,
        tcod.FONT_LAYOUT_ASCII_INROW | tcod.FONT_TYPE_GREYSCALE,
        16, 16
        )
    console = tcod.console_init_root(60, 40, 'Test', False)

    world = ecs.World()
    renderer_sys = RendererSystem(world)

    player = world.new_entity()
    player[Position].add(x=0, y=0)
    player[Graphic].add(ch=ord('@'), fg=(255, 255, 255))

    #console.print_(0, 0, 'Hello World!')
    while not tcod.console_is_window_closed():
        key = tcod.console_wait_for_keypress(False)
        tcod.console_flush()
