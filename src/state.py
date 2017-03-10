
import tcod

import gameobj
import g

class State(object):
    def __init__(self):
        self.__running = False

    def push(self):
        assert not self.__running
        self.__running = True
        while self.__running and not tcod.console_is_window_closed():
            g.world.loop()
            self.on_draw()
            tcod.console_flush()

            key = tcod.Key()
            mouse = tcod.Mouse()
            while tcod.sys_check_for_event(tcod.EVENT_KEY, key, mouse):
                if key.pressed:
                    self.on_key(key)

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

    ord('h'): (-1, 0),
    ord('j'): (0, 1),
    ord('k'): (0, -1),
    ord('l'): (1, 0),
    ord('y'): (-1, -1),
    ord('u'): (1, -1),
    ord('b'): (-1, 1),
    ord('n'): (1, 1),

    ord('.'): (0, 0),
    tcod.KEY_KP5: (0, 0),
    }

class GameState(State):
    def on_key(self, key):
        def inverse_key_const(vk):
            for attr in dir(tcod):
                if attr.startswith('KEY_') and getattr(tcod, attr) == vk:
                    return attr
        print((inverse_key_const(key.vk), key.c, key.text))
        k = key.vk if key.vk != tcod.KEY_CHAR else key.c
        if k in DIR_KEYS:
            g.player.location.move_by(*DIR_KEYS[k])
            g.player.actor.action_time += 100
            g.world.camera = g.player.location.xy
        g.player.actor.schedule()
        g.world.loop()

    def on_draw(self):
        cam_x, cam_y = g.world.camera
        cam_width, cam_height = g.console.width, g.console.height
        cam_x -= cam_width // 2
        cam_y -= cam_height // 2
        g.console.ch[:], g.console.fg[:], g.console.bg[:] = \
            g.world.terrain.get_graphic(cam_x, cam_y, cam_width, cam_height)

        for obj in g.world.objects.area(cam_x, cam_y, cam_width, cam_height):
            if obj.graphic is None:
                continue
            x, y = obj[gameobj.Location].xy
            x -= cam_x
            y -= cam_y
            g.console.ch[y, x] = obj[gameobj.Graphic].ch
            g.console.fg[y, x] = obj[gameobj.Graphic].fg
        tcod.console_flush()

