
import sched
import sparsemap
import terrain

class World(object):
    def __init__(self):
        self.objects = sparsemap.SparseMap()
        self.terrain = terrain.Terrain()
        self.camera = (0, 0)
        self.scheduler = sched.Scheduler()
