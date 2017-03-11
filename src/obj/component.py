
class Component(object):
    def __init__(self, obj, **kargs):
        super().__init__(**kargs)
        self.obj = obj

class Location(Component):
    def __init__(self, location=None, **kargs):
        super().__init__(**kargs)
        self.location = None

    def move(self, x, y):
        self.set((x, y))

    def move_by(self, x, y):
        self.set(self.relative(x, y))

    def relative(self, x, y):
        return self.x + x, self.y + y

    def set(self, location):
        """location can be an (x, y) tuple or another Location object"""
        if self.location:
            self.obj.world.objects[self[:]].remove(self.obj)
        self.location = location
        if self.location:
            self.obj.world.objects[self[:]].append(self.obj)

    def __getitem__(self, key):
        return self.location[key]

    @property
    def x(self):
        return self[0]
    @property
    def y(self):
        return self[1]
    @property
    def yx(self):
        return self[::-1]
    @property
    def xy(self):
        return self[:]


class Graphic(Component):
    def __init__(self, ch=ord('!'), fg=(255, 255, 255), **kargs):
        super().__init__(**kargs)
        self.ch = ch
        self.fg = fg

    def __iter__(self):
        yield self.ch
        yield self.fg

