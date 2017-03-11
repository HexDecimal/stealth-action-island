
import g
import obj.component

class Actor(obj.component.Component):
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
        g.player = self.obj

class ActorTest(Actor):
    def act(self):
        self.obj.location.move_by(0, -1)
        self.action_time += 150
        self.schedule()

