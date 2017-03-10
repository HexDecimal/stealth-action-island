
import sched
import state
import sparsemap
import terrain
import g

class World(object):
    def __init__(self):
        self.objects = sparsemap.SparseMap()
        self.terrain = terrain.Terrain()
        self.camera = (0, 0)
        self.scheduler = sched.Scheduler()

    def loop(self):
        while g.player.actor.is_scheduled:
            self.scheduler.next()