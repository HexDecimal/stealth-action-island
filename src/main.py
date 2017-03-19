
import time

import tcod

import component
import ecs.entity
import state
import g
import world

#FONT = 'data/terminal8x8_gs_ro.png'
FONT = 'data/terminal8x12_gs_ro.png'
TITLE = 'title'

WIDTH = 1024 // 8
HEIGHT = 576 // 12

def main():
    g.model = ecs.entity.Entity(
        terrain=component.TerrainSystem(),
        sparsemap=component.SparseMapSystem(),
        scheduler=component.SchedulerSystem(),
        )
    g.model.add_child(
        ecs.entity.Entity(
            location=component.Location(0, 0, 0),
            graphic=component.Graphic('@'),
            actor=component.Actor(),
            )
        )
    g.camera = ecs.entity.Entity(location=component.Location(0, 0, 0))
    g.model.add_child(g.camera)

    g.model.add_child(
        ecs.entity.Entity(
            location=component.Location(1, 0, 0),
            graphic=component.Graphic('U'),
            actor=component.ActorTest(),
            )
        )

    tcod.console_set_custom_font(
        FONT,
        tcod.FONT_LAYOUT_ASCII_INROW | tcod.FONT_TYPE_GREYSCALE,
        16, 16
        )
    with tcod.console_init_root(WIDTH, HEIGHT, TITLE, False) as g.console:
        tcod.sys_set_fps(60)
        current_state = state.GameState()
        current_state.push()
