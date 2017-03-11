
import obj.component

class GameObj(object):
    def __init__(self, world):
        self.world = world
        self.components = {}
        self.observers = {}
        self.location = obj.component.Location(obj=self)
        self.graphic = obj.component.Graphic(obj=self)
        self.actor = None
