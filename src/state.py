
import tcod

import main
import gameobj

class State(object):
    def __init__(self):
        self.__running = False

    def push(self):
        assert not self.__running
        self.__running = True
        while self.__running and not tcod.console_is_window_closed():
            self.on_draw()
            tcod.console_flush()
            self.on_key(tcod.console_wait_for_keypress(False))

    def pop(self):
        assert self.__running
        self.__running = False

    def on_key(self, key):
        pass

    def on_draw(self):
        pass


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

class GameState(State):
    def on_key(self, key):
        def inverse_key_const(vk):
            for attr in dir(tcod):
                if attr.startswith('KEY_') and getattr(tcod, attr) == vk:
                    return attr
        print((inverse_key_const(key.vk), key.c, key.text))
        if key.vk in DIR_KEYS:
            main.player[gameobj.Location].move_by(*DIR_KEYS[key.vk])
            main.world.camera = main.player[gameobj.Location].xy

    def on_draw(self):
        console = main.console
        world = main.world
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

