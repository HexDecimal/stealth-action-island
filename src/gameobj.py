
import state

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

class Actor(Component):
    def __init__(self, **kargs):
        super().__init__(**kargs)
        self.is_scheduled = False
        self.action_time = 0
        self.schedule()

    def schedule(self):
        assert not self.is_scheduled
        self.is_scheduled = True
        self.obj.world.scheduler.schedule(self.action_time, self)
        self.action_time = 0

    def __call__(self):
        assert self.is_scheduled
        self.is_scheduled = False
        if self.obj.actor is self:
            self.act()

    def act(self):
        pass

class ActorPlayerControl(Actor):
    def act(self):
        pass

class ActorTest(Actor):
    def act(self):
        self.obj.location.move_by(0, -1)
        self.action_time += 150
        self.schedule()

class GameObj(object):
    def __init__(self, world):
        self.world = world
        self.components = {}
        self.observers = {}
        self.location = Location(obj=self)
        self.graphic = Graphic(obj=self)
        self.actor = None

    def __getitem__(self, component_class):
        return getattr(self, component_class.__name__.lower())

    def __contains__(self, component_class):
        return component_class in self.components
