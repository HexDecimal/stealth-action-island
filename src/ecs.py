
from collections import defaultdict


class EntityComponentInterface(object):
    def __init__(self, entity, component_cls):
        self.entity = entity
        self.component_cls = component_cls
        
    def add(self, *args, **kargs):
        return self.component_cls(self.entity, *args, **kargs)
        
    def add_unique(self, *args, **kargs):
        try:
            return self.entity.components[self.component_cls][0]
        except IndexError:
            return self.add(*args, **kargs)
            
    def __iter__(self):
        return iter(self.entity.components[self.component_cls])
        

class Entity(object):
    def __init__(self, world):
        self.world = world
        self.components = defaultdict(list)
        world.entities.add(self)

    def remove(self):
        self.world.entities.remove(self)
        for component in self.components:
            component.remove()
            
    def __getitem__(self, component_cls):
        return EntityComponentInterface(self, component_cls)

class Component(object):
    def __init__(self, entity):
        self.entity = entity
        self.entity.components[self.__class__].append(self)
        self.world.components[self.__class__].add(self)
        self.world.ev_added(self)
        
    @property
    def world(self):
        return self.entity.world

    def remove(self):
        self.world.ev_removed(self)
        self.world.components[self.__class__].remove(self)
        self.entity.components[self.__class__].remove(self)

class System(object):
    def __init__(self, world):
        self.world = world
        world.systems.append(self)

    def remove(self):
        self.world.systems.remove(self)

    def ev_added(self, component):
        pass

    def ev_removed(self, component):
        pass

class World(object):
    def __init__(self):
        self.entities = set()
        self.systems = []
        self.components = defaultdict(set)

    def ev_added(self, component):
        for sys in self.systems:
            sys.ev_added(component)

    def ev_removed(self, component):
        for sys in self.systems:
            sys.ev_removed(component)

    def new_entity(self):
        return Entity(self)
