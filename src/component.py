
import ecs.component
import sched
import terrain
import sparsemap

class TerrainSystem(ecs.component.Component, terrain.Terrain):
    pass


class SchedulerSystem(ecs.component.Component):
    def __init__(self):
        super().__init__()
        self.scheduler = sched.Scheduler()
        self.pending = []
        self.player = None

    def ev_schedule_request(self, actor):
        if actor.entity is self.player:
            return
        assert not actor.is_scheduled
        actor.is_scheduled = True
        self.scheduler.schedule(actor.action_time, actor)

    def run_until_input_is_needed(self):
        if self.player is not None:
            if self.player.actor.action_time == 0:
                return
            self.scheduler.schedule(self.player.actor.action_time,
                                    self.player.actor)
            self.player = None

        while self.player is None:
            self.scheduler.next()


class SparseMapSystem(ecs.component.Component, sparsemap.SparseMap):
    def ev_component_added(self, component):
        if not isinstance(component, Location):
            return
        assert component.entity is not None
        self._objects[component.xyz].append(component.entity)

    def ev_component_removed(self, component):
        if not isinstance(component, Location):
            return
        self._objects[component.xyz].remove(component.entity)

    def ev_location_moved(self, entity, new_xyz, old_xyz):
        self._objects[old_xyz].remove(entity)
        self._objects[new_xyz].append(entity)


class Location(ecs.component.Component):
    def __init__(self, x=0, y=0, z=0):
        super().__init__()
        self.location = self
        self._x = x
        self._y = y
        self._z = z

    def move_to(self, x, y, z=None):
        if z is None:
            z = self.z
        self.entity.propagate_up(
            'ev_location_moved',
            self.entity,
            (x, y, z),
            (self.x, self.y, self.z),
            )
        self.location = self
        self._x = x
        self._y = y
        self._z = z

    def move_by(self, x, y, z=0):
        self.move_to(*self.relative(x, y, z))

    def relative(self, x, y, z=0):
        return self.x + x, self.y + y, self.z + z

    @property
    def x(self):
        return self.location._x
    @property
    def y(self):
        return self.location._y
    @property
    def z(self):
        return self.location._z
    @property
    def yx(self):
        return self.y, self.x
    @property
    def xy(self):
        return self.x, self.y
    @property
    def xyz(self):
        return self.x, self.y, self.z


class Graphic(ecs.component.Component):
    def __init__(self, ch=ord('!'), fg=(255, 255, 255), **kargs):
        super().__init__(**kargs)
        try:
            self.ch = ord(ch)
        except TypeError:
            self.ch = ch
        self.fg = fg

    def __iter__(self):
        yield self.ch
        yield self.fg


class Actor(ecs.component.Component):
    def __init__(self):
        super().__init__()
        self.is_scheduled = False
        self.action_time = 0

    def ev_entity_connected(self, entity):
        self.entity.propagate_up('ev_schedule_request', self)

    def move(self, x, y, z=0):
        self.entity.location.move_by(x, y, z)
        self.action_time += 100

    def __call__(self):
        self.is_scheduled = False
        self.action_time = 0
        self.act()
        self.entity.propagate_up('ev_schedule_request', self)

    def act(self):
        self.entity.root.scheduler.player = self.entity

class ActorTest(Actor):

    def act(self):
        self.move(0, -1)
