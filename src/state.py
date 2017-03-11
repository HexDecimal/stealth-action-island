
import tcod

import g

def inverse_key_const(vk):
    for attr in dir(tcod):
        if attr.startswith('KEY_') and getattr(tcod, attr) == vk:
            return attr
    return chr(vk)

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
                key.vk = key.vk if key.vk != tcod.KEY_CHAR else key.c
                print((inverse_key_const(key.vk), key.c, key.text))
                if key.pressed:
                    self.on_key(key)

    def pop(self):
        assert self.__running
        self.__running = False

    def on_key(self, key):
        pass

    def on_draw(self):
        pass

CANCEL_KEYS = [tcod.KEY_ESCAPE]
MAP_KEYS = [ord('m')]

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
        if key.vk in DIR_KEYS:
            g.player.location.move_by(*DIR_KEYS[key.vk])
            g.player.actor.action_time += 100
            g.world.camera = g.player.location.xy
        if key.vk in MAP_KEYS:
            MapState().push()
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
            x, y = obj.location.xy
            x -= cam_x
            y -= cam_y
            g.console.ch[y, x] = obj.graphic.ch
            g.console.fg[y, x] = obj.graphic.fg
        tcod.console_flush()

class MapState(State):
    def on_key(self, key):
        if key.pressed and key.vk == tcod.KEY_TEXT:
            return
        #if key.vk in CANCEL_KEYS:
        #    self.pop()
        self.pop()

    def on_draw(self):
        g.console.ch[:], g.console.fg[:], g.console.bg[:] = \
            g.world.terrain.get_map_graphic(g.console.width, g.console.height)

